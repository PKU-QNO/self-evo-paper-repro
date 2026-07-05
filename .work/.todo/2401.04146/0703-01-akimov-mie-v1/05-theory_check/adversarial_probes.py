"""step05 theory_check 对抗性探针.

case: 0703-01-akimov-mie-v1 | 审查 scattering.py + akimov_coeffs.py
目的: 不靠 verifier PASS 背书, 独立证伪。覆盖:
  P1 Rayleigh 极限符号对教材解析式核 (含符号, 检时谐/xi 约定)
  P2 负 eps 域 m 纯虚两分支哪支数值有限 (检 sqrt 主值)
  P3 负 eps 角点 (eps=-10,q_e=10,l=3) 系数量级与稳定性
  P4 极点/退化点行为 (分母->0)
  P5 T2 是否伪独立 (源码级检 import + 独立复算一角点)
  P6 大 l (远超 Wiscombe) 行为
  P7 xi 符号翻转注入对照 (若用 -i y, a_l 应取共轭 -> Rayleigh 符号反)
不自写特殊函数, 一律 scipy。
"""
from __future__ import annotations

import sys
import numpy as np
from scipy.special import spherical_jn, spherical_yn

CODE_DIR = "reproduction_test/mie/code"
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from scattering import mie_ab, compute_cross_sections, wiscombe_nmax  # noqa: E402
from akimov_coeffs import akimov_ab  # noqa: E402

SEP = "=" * 70


def _psi(l, z):
    jl = spherical_jn(l, z)
    return z * jl, jl + z * spherical_jn(l, z, derivative=True)


def _xi_sign(l, z, sign):
    """xi_l with h^(1)=j+sign*i*y; sign=+1 正确(e^{-iwt}), sign=-1 错误对照。"""
    jl = spherical_jn(l, z)
    yl = spherical_yn(l, z)
    jlp = spherical_jn(l, z, derivative=True)
    ylp = spherical_yn(l, z, derivative=True)
    h1 = jl + sign * 1j * yl
    h1p = jlp + sign * 1j * ylp
    return z * h1, h1 + z * h1p


def _mie_ab_signed(l, m, x, sign):
    """独立复算 a_l,b_l, xi 符号可选, 用于符号翻转对照。"""
    mx = m * x
    psi_mx, psip_mx = _psi(l, mx)
    psi_x, psip_x = _psi(l, x)
    xi_x, xip_x = _xi_sign(l, x, sign)
    a = (m * psi_mx * psip_x - psi_x * psip_mx) / (m * psi_mx * xip_x - xi_x * psip_mx)
    b = (psi_mx * psip_x - m * psi_x * psip_mx) / (psi_mx * xip_x - m * xi_x * psip_mx)
    return a, b


def probe1_rayleigh_sign():
    print(SEP)
    print("P1: Rayleigh 极限符号 — 对 BH 教材解析式 a_1 = -i(2/3)x^3 (m^2-1)/(m^2+2)")
    print("    (BH 1983 式 4.56/4.57, e^{-iwt}; 符号是 xi 约定的判据, 不靠 verifier)")
    for m in (1.5 + 0j, 2.0 + 0j, 1.2 + 0j):
        for x in (0.01, 0.02):
            a1_code, b1_code = mie_ab(1, m, x)
            m2 = m * m
            a1_ana = -1j * (2.0 / 3.0) * x ** 3 * (m2 - 1) / (m2 + 2)
            rel = abs(a1_code - a1_ana) / abs(a1_ana)
            # 符号一致性: 实部虚部符号同号
            same_sign = (np.sign(a1_code.imag) == np.sign(a1_ana.imag))
            print(f"  m={m.real:.1f} x={x:.3f}: code a1={a1_code:.6e}")
            print(f"                 教材 a1={a1_ana:.6e}  rel={rel:.2e}  Im同号={same_sign}")
    print("  判读: rel<~1e-2(x^5 修正量级) 且 Im 同号 => xi 用 +i y 正确, 时谐 e^{-iwt} 对。")


def probe7_sign_flip_contrast():
    print(SEP)
    print("P7: xi 符号翻转注入对照 — 若代码误用 h=j-i y, a_l 应取共轭 (Rayleigh 符号反)")
    m, x = 1.5 + 0j, 0.02
    a_plus, _ = _mie_ab_signed(1, m, x, +1)   # 正确
    a_minus, _ = _mie_ab_signed(1, m, x, -1)  # 错误对照
    a_code, _ = mie_ab(1, m, x)
    print(f"  code            a1 = {a_code:.6e}")
    print(f"  +i y (正确)     a1 = {a_plus:.6e}")
    print(f"  -i y (错误对照) a1 = {a_minus:.6e}  <- Im 号翻转")
    print(f"  code == +i y ? {abs(a_code-a_plus)<1e-18};  code == conj(-i y 分支)? "
          f"{abs(a_code-np.conj(a_minus))<1e-12}")
    print("  判读: code 与 +i y 分支逐位一致 => 代码确用正确 xi 符号; 错误分支 Im 反号可鉴别。")


def probe2_neg_eps_branch():
    print(SEP)
    print("P2: 负 eps 域 m 纯虚两 sqrt 分支哪支数值有限 (eps=-10, q_e=10, l=3)")
    eps = -10.0
    m_plus = np.sqrt(complex(eps))      # 主值 Im m>=0  => +3.162i
    m_minus = -m_plus                   # 另一分支 Im m<0 => -3.162i
    x = 10.0
    print(f"  m 主值(Im>=0) = {m_plus:.4f} ; 另一分支 = {m_minus:.4f}")
    for tag, m in (("Im m>=0 (主值)", m_plus), ("Im m<0 (错分支)", m_minus)):
        mx = m * x
        psi_mx, psip_mx = _psi(3, mx)
        finite = np.isfinite(psi_mx) and np.isfinite(psip_mx)
        print(f"  {tag}: m*x={mx:.3f}  psi_3(mx)={psi_mx:.3e}  |psi|={abs(psi_mx):.3e}  finite={finite}")
    a, b = mie_ab(3, m_plus, x)
    print(f"  代码 mie_ab(l=3,m=主值,x=10): a={a:.6e} b={b:.6e}  finite={np.isfinite(a) and np.isfinite(b)}")
    print("  判读: Im m>=0 时 j_l(mx) 内含 e^{-Im(mx)... } 有界; Im m<0 指数发散。代码 _refractive_index")
    print("        直接收敛 complex(m), 分支由上游 crosscheck/solver 的 sqrt(主值) 决定 -> 见结论。")


def probe3_neg_eps_corner_magnitude():
    print(SEP)
    print("P3: 负 eps 角点系数量级 (spec 称 |分子|~5e14 仍在 float64 安全范围)")
    for (l, eps, x) in [(3, -10.0, 10.0), (3, -10.0, 8.0), (1, -10.0, 10.0), (2, -10.0, 10.0)]:
        m = np.sqrt(complex(eps))
        a, b = mie_ab(l, m, x)
        a_ak, b_ak = akimov_ab(l, m, x)
        ok = np.isfinite(a) and np.isfinite(b)
        print(f"  l={l} eps={eps} q_e={x}: a={a:.4e} b={b:.4e} finite={ok}  "
              f"|a-a_ak|={abs(a-a_ak):.2e}")
    # 探测原始分子分母绝对量级
    l, eps, x = 3, -10.0, 10.0
    m = np.sqrt(complex(eps))
    mx = m * x
    psi_mx, psip_mx = _psi(l, mx)
    print(f"  raw @ l=3 corner: |psi_3(mx)|={abs(psi_mx):.3e} |psi'_3(mx)|={abs(psip_mx):.3e} "
          f"(float64 max ~1.8e308)")
    print("  判读: 系数有限且 float64 远未溢出 => 负 eps 域数值可用。")


def probe4_pole_behavior():
    print(SEP)
    print("P4: 极点/退化点行为 (分母模长 -> 0, graceful?)")
    # eps_ratio=0 退化点 m=0
    for m in (0.0 + 0j, 1e-8 + 0j):
        try:
            a, b = mie_ab(1, m, 1.0)
            print(f"  m={m}: a={a} b={b} (finite a={np.isfinite(a)})")
        except Exception as e:
            print(f"  m={m}: raised {type(e).__name__}: {e}")
    # 扫描寻找一个真实分母近零点 (loci 附近), 看是否静默给错值
    print("  扫描 l=1 TM eps in [-9,14] q_e in (0,3] 找分母最小模长点:")
    from scattering import _riccati_psi, _riccati_xi  # 内部件用于诊断
    worst = None
    for eps in np.linspace(-9, 14, 400):
        if abs(eps) < 1e-6:
            continue
        m = np.sqrt(complex(eps))
        for x in np.linspace(0.05, 3.0, 200):
            mx = m * x
            psi_mx, psip_mx = _riccati_psi(1, mx)
            xi_x, xip_x = _riccati_xi(1, x)
            aden = abs(m * psi_mx * xip_x - xi_x * psip_mx)
            if worst is None or aden < worst[0]:
                worst = (aden, eps, x)
    print(f"  最小 |a_den| = {worst[0]:.3e} @ eps={worst[1]:.3f} q_e={worst[2]:.3f}")
    m = np.sqrt(complex(worst[1]))
    a, b = mie_ab(1, m, worst[2])
    print(f"  该点 a_1={a:.4e} (|a|={abs(a):.3e})  finite={np.isfinite(a)}")
    print("  判读: 分母最小模长与是否静默给非物理值。scattering 无 try/except, 极点将得 inf/nan(可接受),")
    print("        但绝不 silently 返回有限错值 —— 看上面是否出现异常小分母配异常大 |a|。")


def probe5_t2_independence():
    print(SEP)
    print("P5: T2 是否伪独立 — 用 AST 解析 akimov_coeffs 真实 import (排除 docstring 假阳)")
    import ast
    import inspect
    import akimov_coeffs
    src = inspect.getsource(akimov_coeffs)
    tree = ast.parse(src)
    real_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            real_imports.append(("from", node.module, [a.name for a in node.names]))
        elif isinstance(node, ast.Import):
            real_imports.append(("import", None, [a.name for a in node.names]))
    print(f"  AST 真实 import 语句: {real_imports}")
    imports_scat = any(
        (mod and "scattering" in mod) or any("scattering" in n for n in names)
        for _, mod, names in real_imports
    )
    # 真实调用名 (AST Name/Attribute), 非 docstring 字符串
    called = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    uses_mie_ab = "mie_ab" in called
    print(f"  真实 import 依赖 scattering? {imports_scat}  (docstring 里提及不算)")
    print(f"  真实代码调用 mie_ab? {uses_mie_ab}")
    # 独立第三实现 (完全另写 Riccati, 只用 scipy) 复算一角点, 三方比对
    def third_ab(l, m, x):
        # 用 modified 组合独立写: xi via psi + i*chi, chi=-z*y
        def psi(z):
            jl = spherical_jn(l, z)
            return z * jl, jl + z * spherical_jn(l, z, derivative=True)
        def chi(z):
            yl = spherical_yn(l, z)
            return -z * yl, -(yl + z * spherical_yn(l, z, derivative=True))
        mx = m * x
        p_mx, pp_mx = psi(mx)
        p_x, pp_x = psi(x)
        c_x, cp_x = chi(x)
        xi_x = p_x - 1j * c_x
        xip_x = pp_x - 1j * cp_x
        a = (m * p_mx * pp_x - p_x * pp_mx) / (m * p_mx * xip_x - xi_x * pp_mx)
        b = (p_mx * pp_x - m * p_x * pp_mx) / (p_mx * xip_x - m * xi_x * pp_mx)
        return a, b
    for (l, eps, x) in [(2, -3.0, 1.5), (3, 5.0, 4.0), (1, -8.0, 9.0)]:
        m = np.sqrt(complex(eps))
        a_bh, _ = mie_ab(l, m, x)
        a_ak, _ = akimov_ab(l, m, x)
        a_3, _ = third_ab(l, m, x)
        print(f"  l={l} eps={eps} q_e={x}: |BH-Ak|={abs(a_bh-a_ak):.2e} |BH-3rd(xi=psi-i chi)|={abs(a_bh-a_3):.2e}")
    print("  判读: 无 import 且三条独立路径(BH / Akimov 显式 q 因子 / xi=psi-i*chi 形式)一致 => 真独立。")


def probe6_large_l():
    print(SEP)
    print("P6: 大 l 行为 (远超 Wiscombe nmax), 看 evanescent 高阶是否 graceful")
    m, x = 1.5 + 0j, 5.0
    nmax = wiscombe_nmax(x)
    print(f"  x={x} Wiscombe nmax={nmax}; 探测 l 直到远超:")
    for l in [nmax, nmax + 10, nmax + 40, nmax + 80]:
        a, b = mie_ab(l, m, x)
        print(f"    l={l}: a={a:.3e} b={b:.3e} finite={np.isfinite(a) and np.isfinite(b)}")
    print("  判读: 高阶 a_l 应 ->0 或渐小/underflow, 不得爆 inf/nan 于收敛区内 (l<nmax)。")


def probe8_m_even_symmetry():
    print(SEP)
    print("P8: a_l/b_l 是否为 m 的偶函数 (决定负 eps 域 sqrt 分支选择是否影响系数)")
    print("    解析: psi_l(-z)=(-1)^{l+1}psi_l(z), psi'_l(-z)=(-1)^l psi'_l(z)")
    print("    => a_l(-m)=[(-1)^l 分子]/[(-1)^l 分母]=a_l(m). 若成立, 主值/负分支等价。")
    maxdiff = 0.0
    for (l, eps, x) in [(1, -10.0, 10.0), (2, -5.0, 3.0), (3, -10.0, 8.0),
                        (1, 5.0, 2.0), (3, -2.0, 1.07)]:
        mp = np.sqrt(complex(eps))      # 主值 Im>=0
        mm = -mp                        # 负分支 Im<0
        a_p, b_p = mie_ab(l, mp, x)
        a_m, b_m = mie_ab(l, mm, x)
        d = max(abs(a_p - a_m), abs(b_p - b_m))
        maxdiff = max(maxdiff, d)
        print(f"  l={l} eps={eps} q_e={x}: |a(+m)-a(-m)|={abs(a_p-a_m):.2e} "
              f"|b(+m)-b(-m)|={abs(b_p-b_m):.2e}")
    print(f"  max |系数(+m)-系数(-m)| = {maxdiff:.2e}")
    print("  判读: ~0 => a_l,b_l 是 m 偶函数, 负 eps 域 sqrt 主值分支选择不影响系数值,")
    print("        消解 spec 关于'分支取错发散'的顾虑(真发散仅当 |Im(mx)|>~700 溢出, Fig3 域内 <40)。")


def main():
    print("adversarial_probes.py — step05 theory_check 对抗性探针原始 stdout")
    print(f"numpy {np.__version__}")
    probe1_rayleigh_sign()
    probe7_sign_flip_contrast()
    probe2_neg_eps_branch()
    probe3_neg_eps_corner_magnitude()
    probe4_pole_behavior()
    probe5_t2_independence()
    probe6_large_l()
    probe8_m_even_symmetry()
    print(SEP)
    print("END probes")


if __name__ == "__main__":
    main()

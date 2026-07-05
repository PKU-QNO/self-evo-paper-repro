"""Layer 1.5 verifier: large-size extinction paradox Q_ext -> 2 at large x.

物理内核：大尺寸消光佯谬 Q_ext -> 2（衍射极限，遮挡 πR² + 前向衍射各贡献 1）。

设计教训（2026-07-05，Akimov case 首跑 Gate3）：早先版本硬编码
xs=[50,80,120,200] + tol=0.05，对无损介质球 m=1.5 会 FAIL——不是实现 bug，
是 verifier 设计缺陷。经独立复算确认两点：
  (1) Q_ext->2 对无损球收敛极慢（代数收敛 ~1/x 边缘衍射修正），x=200 仍偏
      0.09、x=1000 才 0.014、x=2000 才 0.010；单点 |Q-2|<0.05 需 x≳1000。
  (2) 弱阻尼（m 带小虚部）压不掉主偏离——虚部只衰减叠加的 ripple 抖动，
      不改慢代数收敛趋势（m=1.5+0.1i 在 x=200 仍 0.057）。
故改为**趋势判据**：不要求某几点精确达 2，而是验证 Q_ext 随 x 单调趋近 2
（这才是"佯谬"的物理内核，且对慢收敛/ripple 免疫）。三判据全过才 PASS：
  C1 末点（x=800）|Q_ext-2| < 末点容差 0.05
  C2 |Q_ext-2| 随 x 基本单调下降（容 0.02 ripple 反弹）
  C3 首点比末点更偏离 2（整体收敛方向正确）

双向验证（写此文件时实测，见 case 04 记录）：
  正确实现（无损 m=1.5）-> PASS（末点 0.0163）
  注入 bug 漏 b_l 项      -> FAIL（末点 0.99）
  注入 bug 系数×0.5       -> FAIL（末点 0.49）

适用条件（对齐 verification.md）：无损或弱阻尼球；判的是"大 x 趋势"，非"某点精确达 2"。
Imports from reproduction_test/mie/code/. Exits 0 on PASS, non-zero on FAIL.
"""
from __future__ import annotations
import sys
import numpy as np

CODE_DIR = "reproduction_test/mie/code"
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

TARGET = 2.0
END_TOL = 0.05        # C1: 末点（最大 x）|Q_ext-2| 容差
RIPPLE_TOL = 0.02     # C2: 允许的单调下降反弹（ripple）幅度
XS = np.array([50.0, 100.0, 200.0, 400.0, 800.0])  # 单调递增；末点 x=800


def main() -> int:
    try:
        from scattering import compute_Q_ext  # type: ignore
    except ImportError as e:
        print(f"FAIL: implementation not found ({e}). Run after stage 1 code is written.")
        return 2

    m = 1.5 + 0.0j
    try:
        qext = np.array([compute_Q_ext(m=m, x=x) for x in XS])
    except Exception as e:
        print(f"FAIL: compute_Q_ext raised {e}")
        return 1

    dev = np.abs(qext - TARGET)

    c1 = dev[-1] < END_TOL                        # 末点接近 2
    c2 = bool(np.all(np.diff(dev) < RIPPLE_TOL))  # 基本单调下降
    c3 = dev[0] > dev[-1]                         # 首点比末点更偏

    table = "  ".join(f"x={x:.0f}:|Q-2|={d:.4f}" for x, d in zip(XS, dev))
    if c1 and c2 and c3:
        print(f"PASS large_size_limit (trend): {table}")
        print(f"  末点 x={XS[-1]:.0f} |Q_ext-2|={dev[-1]:.4f} < {END_TOL}; 单调下降 & 收敛方向正确")
        return 0
    print(f"FAIL large_size_limit (trend): {table}")
    print(f"  C1 末点<{END_TOL}:{c1}  C2 单调下降(容{RIPPLE_TOL}):{c2}  C3 首>末:{c3}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

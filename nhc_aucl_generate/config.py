# ========== 全局路径 ==========
OUTPUT_DIR = "results"
FAILED_CSV = "failed.csv"

# 外部程序路径
XTB_EXECUTABLE = "~/anaconda3/envs/molsimp/bin/xtb"
CREST_EXECUTABLE = "~/anaconda3/envs/molsimp/bin/crest"

# ========== 计算参数 ==========
AU_C_DIST = 2.00     # Au–C 键长 (Å)
CL_DIST = 2.32       # Au–Cl 键长 (Å)
NUM_DIRS = 600       # AuCl 插入时的方向采样数
TEMPERATURE = 298    # CREST 采样温度
GFIN_METHOD = "2"    # GFN-xTB 模型 (gfn0, gfn1, gfn2, gfnff)

# ========== 并行设置 ==========
USE_HALF_CORES = True

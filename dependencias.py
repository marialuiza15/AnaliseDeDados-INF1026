import subprocess
import sys
 
# ─── Instalação automática das dependências ───────────────────────────────────
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
 
install("kagglehub[pandas-datasets]")
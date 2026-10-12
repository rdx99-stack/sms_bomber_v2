#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════
#   🔥 RDX TOOLS ULTIMATE — ONE-CLICK INSTALLER 🔥
#           Created by: RDX HUNTER
# ═══════════════════════════════════════════════════════

clear

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║    🔥 RDX TOOLS ULTIMATE — SETUP STARTING 🔥    ║"
echo "║           Created by: RDX HUNTER                 ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ═════════════════════════════════════════════════════
# CONFIG — আপনার GitHub Username বসান
# ═════════════════════════════════════════════════════
GITHUB_USER="RDX-HUNTER"
REPO_NAME="rdx_tool"
BRANCH="main"

TOOL_URL="https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/${BRANCH}/rdx_tool.py"
REQ_URL="https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/${BRANCH}/requirements.txt"

# ─────────────────────────────────────────────────────
echo "⏳ [1/5] Updating Termux..."
pkg update -y > /dev/null 2>&1
pkg upgrade -y > /dev/null 2>&1
echo "✅ Termux updated!"
echo ""

# ─────────────────────────────────────────────────────
echo "⏳ [2/5] Installing Python, pip, git, wget..."
pkg install python python-pip git wget -y > /dev/null 2>&1
echo "✅ Python installed!"
echo ""

# ─────────────────────────────────────────────────────
echo "⏳ [3/5] Creating ~/rdx_tool folder..."
cd ~
mkdir -p rdx_tool
cd rdx_tool
echo "✅ Folder ready: ~/rdx_tool"
echo ""

# ─────────────────────────────────────────────────────
echo "⏳ [4/5] Downloading files..."
wget -q "$REQ_URL" -O requirements.txt 2>/dev/null
if [ ! -s "requirements.txt" ]; then
    echo "aiohttp" > requirements.txt
    echo "requests" >> requirements.txt
    echo "urllib3" >> requirements.txt
fi

wget -q "$TOOL_URL" -O rdx_tool.py 2>/dev/null
if [ -s "rdx_tool.py" ]; then
    echo "✅ Files downloaded!"
else
    echo "⚠️  Download failed — checking local..."
    if [ -f "/storage/emulated/0/rdx_tool/rdx_tool.py" ]; then
        cp /storage/emulated/0/rdx_tool/rdx_tool.py ~/rdx_tool/
        echo "✅ Copied from local storage!"
    fi
fi
echo ""

# ─────────────────────────────────────────────────────
echo "⏳ [5/5] Installing Python packages..."
pip install --upgrade pip > /dev/null 2>&1
pip install aiohttp requests urllib3 > /dev/null 2>&1
echo "✅ Dependencies installed!"
echo ""

# ─────────────────────────────────────────────────────
# Alias Setup
# ─────────────────────────────────────────────────────
grep -q "alias rdx=" ~/.bashrc 2>/dev/null || \
    echo "alias rdx='cd ~/rdx_tool && python rdx_tool.py'" >> ~/.bashrc

# ─────────────────────────────────────────────────────
echo "╔══════════════════════════════════════════════════╗"
echo "║        ✅ SETUP COMPLETE!                        ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║   📁 Location: ~/rdx_tool                        ║"
echo "║   🚀 Run: type  rdx   or  python rdx_tool.py     ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "🔥 Starting Tool in 3 seconds... 🔥"
sleep 3
cd ~/rdx_tool
python rdx_tool.py

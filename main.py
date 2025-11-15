# =============================================================================
# Copyright (c) 2025 Little Tree Studio
# 
# This program and all associated documentation and files are protected by
# the Eclipse Public License 2.0. You may obtain a complete copy of this
# license at:
# 
#     https://www.eclipse.org/legal/epl-2.0/
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is provided on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
File Description
==============================================================================
The main entry point for the DashWidgets application.

@author: Little Tree Studio
@contact: studio@zsxiaoshu.cn
@organization: https://zsxiaoshu.cn/
@project: DashWidgets
@repository: https://github.com/Little-Tree-Studio/DashWidgets
@license: Eclipse Public License 2.0 (EPL-2.0)
@copyright: Copyright (c) 2025 Little Tree Studio. All rights reserved.
"""

# SPDX-License-Identifier: EPL-2.0
# Identifier Note: SPDX (Software Package Data Exchange) license identifier
# for automated license identification tools

# =============================================================================
# Development Team Information
# =============================================================================
# Primary Developer  : Little Tree Studio
# Contact Email      : studio@zsxiaoshu.cn
# Official Website   : https://zsxiaoshu.cn/
# Project Homepage   : https://github.com/Little-Tree-Studio/DashWidgets
# Issue Tracker      : https://github.com/Little-Tree-Studio/DashWidgets/issues
# Documentation      : https://github.com/Little-Tree-Studio/DashWidgets/wiki
# 
# Technical Support  : support@zsxiaoshu.cn
# Business Inquiries : business@zsxiaoshu.cn
# =============================================================================

# =============================================================================
# License Compliance Statement
# =============================================================================
# IMPORTANT NOTICE:
# 1. This file is open source software under the Eclipse Public License 2.0
# 2. You may freely use, modify, and distribute this software subject to EPL 2.0 terms
# 3. If you distribute this software as a standalone application, you must
#    release the source code under the same license
# 4. If you link this software as a library/module to your proprietary software,
#    this restriction does not apply
# 5. All modified files must retain this copyright notice and license information
# 6. Distribution must include a means to obtain the complete license text
# 
# Full legal terms available at: https://www.eclipse.org/legal/epl-2.0/
# =============================================================================



__author__ = "Little Tree Studio"
__copyright__ = "Copyright (c) 2025 Little Tree Studio"
__license__ = "EPL-2.0"
__version__ = "1.0.0"
__maintainer__ = "Little Tree Studio"
__email__ = "studio@zsxiaoshu.cn"
__status__ = "Development"  # Development/Testing/Production
__project__ = "DashWidgets"
__repository__ = "https://github.com/Little-Tree-Studio/DashWidgets"
__website__ = "https://zsxiaoshu.cn/"


import maliang
from loguru import logger
from maliang import toolbox
from maliang.core import configs

def load_fonts():
    if toolbox.load_font("./assets/fonts/HarmonyOS_Sans_SC_Regular.ttf"):
        configs.Font.family = "HarmonyOS Sans SC"
        logger.info("Loaded font: HarmonyOS Sans SC Regular")
    else:
        logger.warning("Failed to load font: HarmonyOS Sans SC Regular")
def main_window():
    root = maliang.Tk(title="DashWidgets 主窗口", icon="./assets/images/icon.ico")
    
    main_canvas = maliang.Canvas(root, width=1080, height=720)
    main_canvas.place(x=0, y=0)
    
    maliang.Text(main_canvas, text="Hello, DashWidgets!", position=(5,5),fontsize=24)
    
    root.mainloop()


if __name__ == "__main__":
    load_fonts()
    main_window()

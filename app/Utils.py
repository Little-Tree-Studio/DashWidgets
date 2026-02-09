from loguru import logger
from maliang import toolbox
from maliang.core import configs
from .path import FONTS_PATH

def load_fonts():
    if toolbox.load_font(str(FONTS_PATH / "HarmonyOS_Sans_SC_Regular.ttf")):
        configs.Font.family = "HarmonyOS Sans SC"
        logger.info("Loaded font: HarmonyOS Sans SC Regular")
    else:
        logger.warning("Failed to load font: HarmonyOS Sans SC Regular")
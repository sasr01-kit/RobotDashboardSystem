import battery100 from "../assets/battery_100.svg";
import battery80 from "../assets/battery_80.svg";
import battery60 from "../assets/battery_60.svg";
import battery20 from "../assets/battery_20.svg";
import battery0 from "../assets/battery_0.svg";

/* Map for dynamic minimized battery icons */

export const BATTERY_ICONS = {
  100: battery100,
  80: battery80,
  60: battery60,
  20: battery20,
  0: battery0
};


export const getBatteryIcon = (level) => {
  if (level > 80) return BATTERY_ICONS[100];
  if (level > 60) return BATTERY_ICONS[80];
  if (level > 30) return BATTERY_ICONS[60];
  if (level > 5) return BATTERY_ICONS[20];
  return BATTERY_ICONS[0];
};


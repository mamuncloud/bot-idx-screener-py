import pandas as pd
import argparse
import os
from cmd import Command

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IDX Stock Screener CLI")
    parser.add_argument(
        "--strategy", 
        choices=[
          "macd_cross_up",
          "rising_three",
          "trend_following",
          "breakout_20_days",
          "bb_breakout_volume"
        ],
        required=True,
        help="Choose the screening strategy"
    )
    
    args = parser.parse_args()

    cmd = Command()
    cmd.run(args.strategy)

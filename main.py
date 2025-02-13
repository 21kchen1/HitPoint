import logging
from View.View import View

# 日志设置
logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(funcName)s . %(message)s',
                    level=logging.INFO)

def main() -> None:
    view = View()
    view.run()

if __name__ == "__main__":
    main()
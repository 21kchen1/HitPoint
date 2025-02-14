import logging
from View.View import View
from Service.Service import Servcie
from Controller.Controller import Controller

# 日志设置
logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(funcName)s . %(message)s',
                    level=logging.INFO)

def main() -> None:
    # 视图
    view = View()
    # 服务
    service = Servcie()
    # 控制器
    controller = Controller(view, service)
    view.run()

if __name__ == "__main__":
    main()
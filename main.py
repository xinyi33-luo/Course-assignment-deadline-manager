def main():
    while True:
        print("\n===== 课程作业截止日期管理器 =====")
        print("1. 添加作业")
        print("2. 查看全部作业")
        print("3. 查看未完成作业")
        print("4. 标记作业完成")
        print("5. 查看统计")
        print("0. 退出")

        choice = input("请选择：").strip()

        if choice == "0":
            print("再见！")
            break
        else:
            print("这个功能还没做，先选 0 退出。")


if __name__ == "__main__":
    main()
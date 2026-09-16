import json
import os
from datetime import datetime

# 数据文件路径
DATA_FILE = os.path.join("data", "assignments.json")


def load_assignments():
    """从 JSON 文件读取作业列表。文件不存在或出错时返回空列表。"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("警告：数据文件读取失败，本次将使用空列表。")
        return []


def save_assignments(assignments):
    """把作业列表写回 JSON 文件。"""
    # 确保 data 文件夹存在
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(assignments, f, ensure_ascii=False, indent=2)


def days_left(due_date_str):
    """计算距离截止日期还有几天。已逾期返回负数。"""
    today = datetime.now().date()
    due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    return (due - today).days


def format_deadline(due_date_str):
    """把剩余天数转成易读文字。"""
    days = days_left(due_date_str)
    if days > 0:
        return f"还剩 {days} 天"
    elif days == 0:
        return "今天截止"
    else:
        return f"已逾期 {abs(days)} 天"


def add_assignment():
    """让用户输入一条新作业并保存。"""
    print("\n--- 添加作业 ---")
    course = input("课程名：").strip()
    title = input("作业标题：").strip()
    due_date = input("截止日期（格式 2026-09-20）：").strip()

    # 检查日期格式
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("日期格式不对，请用 2026-09-20 这种格式。添加失败。")
        return

    hours_str = input("预计工时（小时，可留空）：").strip()
    if hours_str == "":
        hours = 0.0
    else:
        try:
            hours = float(hours_str)
        except ValueError:
            print("工时必须是数字，添加失败。")
            return

    if course == "" or title == "":
        print("课程名和作业标题不能为空，添加失败。")
        return

    new_item = {
        "course": course,
        "title": title,
        "due_date": due_date,
        "hours": hours,
        "done": False,
    }

    assignments = load_assignments()
    assignments.append(new_item)
    save_assignments(assignments)
    print(f"已添加：{course} - {title}")


def view_assignments(only_undone=False):
    """查看作业。only_undone=True 时只显示未完成的。"""
    assignments = load_assignments()

    if only_undone:
        assignments = [a for a in assignments if not a["done"]]
        title_text = "未完成作业"
    else:
        title_text = "全部作业"

    print(f"\n--- {title_text} ---")

    if not assignments:
        print("目前没有作业记录。")
        return

    # 按截止日期排序
    assignments.sort(key=lambda a: a["due_date"])

    for i, a in enumerate(assignments, start=1):
        status = "已完成" if a["done"] else "未完成"
        deadline_text = format_deadline(a["due_date"])
        print(f"{i}. [{status}] {a['course']} - {a['title']}")
        print(f"   截止：{a['due_date']}（{deadline_text}）  预计工时：{a['hours']} 小时")


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

        if choice == "1":
            add_assignment()
        elif choice == "2":
            view_assignments(only_undone=False)
        elif choice == "3":
            view_assignments(only_undone=True)
        elif choice == "4":
            print("这个功能还没做。")
        elif choice == "5":
            print("这个功能还没做。")
        elif choice == "0":
            print("再见！")
            break
        else:
            print("请输入 0 到 5 之间的数字。")


if __name__ == "__main__":
    main()
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

def mark_done():
    """让用户选择一条未完成作业，标记为已完成。"""
    assignments = load_assignments()
    undone = [a for a in assignments if not a["done"]]

    if not undone:
        print("\n没有未完成的作业。")
        return

    # 排序，保证编号和"查看未完成作业"一致
    undone.sort(key=lambda a: a["due_date"])

    print("\n--- 选择要标记完成的作业 ---")
    for i, a in enumerate(undone, start=1):
        print(f"{i}. {a['course']} - {a['title']}（截止：{a['due_date']}）")

    choice = input("请输入编号（直接回车取消）：").strip()

    if choice == "":
        print("已取消。")
        return

    try:
        index = int(choice)
    except ValueError:
        print("请输入数字。")
        return

    if index < 1 or index > len(undone):
        print("编号超出范围。")
        return

    # 取出用户选中的那一条
    selected = undone[index - 1]

    # 在原始列表里找到它并改成已完成
    for a in assignments:
        if a is selected:
            a["done"] = True
            break

    save_assignments(assignments)
    print(f"已完成：{selected['course']} - {selected['title']}")

def show_statistics():
    """显示作业统计信息。"""
    assignments = load_assignments()

    print("\n--- 统计 ---")

    if not assignments:
        print("目前没有作业记录。")
        return

    total = len(assignments)
    done_count = sum(1 for a in assignments if a["done"])
    undone_count = total - done_count

    # 逾期：未完成，且剩余天数小于 0
    overdue_count = sum(
        1 for a in assignments
        if not a["done"] and days_left(a["due_date"]) < 0
    )

    rate = done_count / total * 100

    print(f"总作业数：{total}")
    print(f"已完成：{done_count}")
    print(f"未完成：{undone_count}")
    print(f"逾期：{overdue_count}")
    print(f"完成率：{rate:.1f}%")

    # 未完成作业的总预计工时
    pending_hours = sum(
        a["hours"] for a in assignments if not a["done"]
    )
    print(f"未完成作业总预计工时：{pending_hours:.1f} 小时")

    # 每门课的统计
    print("\n按课程统计：")
    courses = {}
    for a in assignments:
        name = a["course"]
        if name not in courses:
            courses[name] = {"total": 0, "done": 0}
        courses[name]["total"] += 1
        if a["done"]:
            courses[name]["done"] += 1

    for name, info in sorted(courses.items()):
        t = info["total"]
        d = info["done"]
        print(f"  {name}：共 {t} 条，已完成 {d} 条（{d/t*100:.0f}%）")

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
            mark_done()
        elif choice == "5":
            show_statistics()
        elif choice == "0":
            print("再见！")
            break
        else:
            print("请输入 0 到 5 之间的数字。")


if __name__ == "__main__":
    main()
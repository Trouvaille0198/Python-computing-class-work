from random import randint
import copy


def Count(M, N):
    monthDate = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    classList = list()  # 记录所有班级的全部生日信息
    classBirthday = list()  # 记录1个班级的生日情况
    for i in range(M):
        for j in range(N):
            month = randint(1, 12)  # 随机生成月份
            birthday = (month, randint(1, monthDate[month - 1]))  # 生成一个人的生日
            classBirthday.append(birthday)  # 获得一个班的生日
        classList.append(copy.deepcopy(classBirthday))  # 将随机生成的班级生日情况加入到班级列表中
        classBirthday.clear()

    sameBirthdayCount = 0  # 统计有相同生日的班级数目
    for i in range(M):
        for x in classList[i]:
            # 一个班级中一个生日出现次数大于两次则说明有相同生日
            if classList[i].count(x) >= 2:
                sameBirthdayCount += 1
                break
    return sameBirthdayCount / M  # 返回相同生日班级数占总班级数比例


def main():
    m = int(input('请输入班级数量：'))
    n = int(input('请输入班级人数：'))
    rate = Count(m, n)
    # 格式化输出
    print('{rate:.2f}%'.format(rate=rate * 100))


if __name__ == '__main__':
    main()
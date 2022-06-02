class TriangleChecker:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def is_triangle(self):
        if isinstance(self.a, (int, float)) and isinstance(self.b, (int, float)) and isinstance(self.c, (int, float)):
            if self.a >= 0 and self.b >= 0 and self.c >= 0:
                lst = []
                lst.append(self.a)
                lst.append(self.b)
                lst.append(self.c)
                lst.sort()
                if lst[0]+lst[1]<= lst[2]:
                    return "С этого нельзя построить."
                else:
                    return "Ура, можно построить треугольник!"
            else:
                return "С отрицательными числами ничего не выйдет!"
        else:
            return "Нужно вводить числа!"

triangle1 = TriangleChecker(4, 3, 6)
print(triangle1.is_triangle())
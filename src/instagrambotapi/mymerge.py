class Merge:
    def __init__(self, list1, list2):
        super().__init__()
        self.final = []
        self.list1 = list1
        self.list2 = list2
    def check_in_list2(self, el):
        for member in self.list1:
            if member == el:
                return True
            else:
                continue
        return False
    def merge(self):
        for member in self.list1:
            self.final.append(member)
        for member in self.list2:
            if not self.check_in_list2(member):
                self.final.append(member)
        return self.final

if __name__ == "__main__":
    a = [2,3,456,63,45,64,65, 534]
    b = [4, 6, 9, 23, 64, 2]
    c = [6, 56, 63, 1480, 1744, 1354, 7]
    final = []
    final = Merge(Merge(a, b).merge(), c).merge()
    final.sort()
    print(final)

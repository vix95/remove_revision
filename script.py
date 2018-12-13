import pandas as pd


# Customer
class Cust1:
    @staticmethod
    def execute(item):
        if item[:2] == "PO":
            return EFGH.execute(item)
        else:
            # check if NPI
            if item[:2] == "LA":
                return item[:3] + ABCD.execute(item[3:])
            else:
                return ABCD.execute(item)  # ABCD/IJKL


class Cust2:
    @staticmethod
    def execute(item):
        if item[:4] == "CDEF":
            return CDEF.execute(item)  # CDEF
        else:
            return MNOP.execute(item)  # MNOP


class Cust3:
    @staticmethod
    def execute(item):
        return QRST.execute(item)


class Cust4:
    @staticmethod
    def execute(item):
        return UVWX.execute(item)


class Cust5:
    @staticmethod
    def execute(item):
        return YZAB.execute(item)


# Prefix
class ABCD:
    @staticmethod
    def execute(item):
        if item[:2] == "11":
            if len(item) == 12:
                return item[:9]
            else:
                return item[:10]

        elif item[:2] == "55":
            return item[:9]

        elif item[:2] == "99":
            return item[:6]
        else:
            return


class EFGH:
    @staticmethod
    def execute(item):
        return item[:len(item) - 10]


class IJKL:
    @staticmethod
    def execute(item):
        if item[:2] == "11":
            if len(item) == 12:
                return item[:9]
            else:
                return item[:10]

        elif item[:2] == "55":
            return item[:9]

        elif item[:2] == "99":
            return item[:6]
        else:
            return


class MNOP:
    @staticmethod
    def execute(item):
        count = 0

        for x in reversed(item):
            if count == 9:
                return

            if x == "R":
                return item[:-count - 1]

            count = count + 1

        return


class QRST:
    @staticmethod
    def execute(item):
        count = 0

        for x in reversed(item):
            if x == ".":
                return item[:-count - 1]

            count = count + 1

        return


class UVWX:
    @staticmethod
    def execute(item):
        count = 0

        for x in reversed(item):
            if x == ".":
                return item[:-count - 4]

            count = count + 1

        return


class YZAB:
    @staticmethod
    def execute(item):
        return item[:9]


class CDEF:
    @staticmethod
    def execute(item):

        if len(item) == 27:
            return '-' + item[16:]

        elif len(item) == 28:
            return '-' + item[15:]

        else:
            count = 0

            for x in reversed(item):
                if count == 9:
                    return

                if x == "-":
                    return item[:-count - 1]

                count = count + 1

        return


# strategy pattern
class RemoveRevision:
    def __init__(self, customer, prefix):
        self.CustomerList = customer
        self.PrefixList = prefix
        self.CustomerHashTable = []
        self.PrefixHashTable = []

    def add_customer(self, customer):
        self.CustomerHashTable.append(customer)

    def add_prefix(self, prefix):
        self.PrefixHashTable.append(prefix)

    def run(self):

        # check if exist prefix in array
        if Item.full[:4] in self.PrefixList:
            Item.prefix = Item.full[:4]
            Item.item = Item.full[4:]
            index = self.PrefixList.index(Item.prefix)
            # check '-'
            if Item.item[:1] == "-":
                Item.separator = Item.item[:1]
                Item.item_rev = Item.item = Item.item[1:]
            else:
                # check if NPI
                if Item.item[:2] == "LA":
                    Item.NPI = Item.item[:2]
                    Item.item = Item.item[2:]
                    # check '-'
                    if Item.item[:1] == "-":
                        Item.separator = Item.full[:1]
                        Item.item_rev = Item.item = Item.item[1:]
                    else:
                        Item.item_rev = Item.item
                else:
                    Item.item_rev = Item.item

            Item.item = self.PrefixHashTable[index].execute(Item.item_rev)
            Item.revision = Item.item_rev[len(Item.item):]
            return True
        else:
            # check if exist customer in array
            if Item.customer in self.CustomerList:
                index = self.CustomerList.index(Item.customer)
                Item.item = self.CustomerHashTable[index].execute(Item.item_rev)

                if Item.item is None:
                    return False
                else:
                    return True

        return False


class MaterialCode(object):
    customer = ""
    full = ""
    item_rev = ""
    item = ""
    prefix = ""
    revision = ""
    separator = ""
    NPI = ""

    def __init__(self, customer, item):
        self.customer = customer
        self.full = item


if __name__ == "__main__":
    program = RemoveRevision(['cust1', 'cust2', 'cust3', 'cust4', 'cust5'],
                             ['ABCD', 'EFGH', 'IJKL', 'MNOP', 'QRST', 'UVWX', 'YZAB', 'CDEF'])

    program.add_customer(Cust1())
    program.add_customer(Cust2())
    program.add_customer(Cust3())
    program.add_customer(Cust4())
    program.add_customer(Cust4())

    program.add_prefix(ABCD())
    program.add_prefix(EFGH())
    program.add_prefix(IJKL())
    program.add_prefix(MNOP())
    program.add_prefix(QRST())
    program.add_prefix(UVWX())
    program.add_prefix(YZAB())
    program.add_prefix(CDEF())

    # pandas IO
    df = pd.read_csv('items.csv', sep="|")
    # df.loc[df.index[0], 'customer_item'] = ""
    failed = 0  # % of failed remove revision
    for i in df.index:
        # df.loc[df.index[i], 'customer_item'] = ""
        try:
            Item = MaterialCode("".lower(), df.loc[df.index[i], 'item'])
            if program.run():
                df.loc[df.index[i], 'item_no_rev'] = Item.prefix + Item.NPI + Item.separator + Item.item
            else:
                # print("Empty: " + df.loc[df.index[i], 'item'])
                df.loc[df.index[i], 'item_no_rev'] = None
                failed += 1

        except TypeError:
            # print("Empty: " + df.loc[df.index[i], 'item'])
            df.loc[df.index[i], 'item_no_rev'] = None
            failed += 1

    # print(df)
    df.to_csv('items.csv', sep="|", index=False)
    print("success: " + "{:.4%}".format((len(df) - failed) / len(df)) +
          "\nrecords: " + str(len(df)) +
          "\nsuccess remove rev: " + str(len(df) - failed) +
          "\nfailed remove rev: " + str(failed))

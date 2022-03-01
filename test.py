import pyupbit

access = "KBbtDnP83wwmXbE4KFG3emL9TOSBP0G0FfahDhWG"          # 본인 값으로 변경
secret = "xepuc8vrxNJNMdfxiCn57vxe5f2aLrxlzHSlTkc0"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
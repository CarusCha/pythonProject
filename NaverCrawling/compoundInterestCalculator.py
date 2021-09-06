from math import pow

# FV = PV * (1 + r)**n  미래가치 = 현재가치 * (1 + 이자율(수익률))**기간


# def compoundInterest(pv, r, n):
#     return pv * ((1 + r) ** n)



# def calculate(pv, r, n):
#     for i in range(1,n+1):
#         fv = compoundInterest(pv, r, i)
#         income = fv - compoundInterest(pv, r, i-1)
#         rate = (fv - pv) / pv * 100
#         print(f'{i} 수익:{round(income)}, 총금액:{round(fv)}, 수익률:{round(rate, 2)}%, 원금:{pv}')


# def compoundInterest(pv, r, n):
#     pv = pv
#     for i in range(1, n + 1):
#         pv = pv + (pv * r)
#         print(pv)
#     return pv
#
# compoundInterest(12000000, 0.5, 5)


# def calculate(pv, r, n, s):
#     originPrice = pv
#     newpv = pv
#     for i in range(1,n+1):
#         originPrice += s
#         before = newpv
#         newpv = newpv + s
#         newpv = newpv + (newpv * r)
#         fv = newpv
#         income = fv - before - s
#         rate = (fv - originPrice) / originPrice * 100
#         # finalRate = (fv - pv) / pv * 100
#         try:
#             finalRate = (fv - pv) / pv * 100
#         except:
#             finalRate = 0
#         # print(f'{i} 수익:{income}, 총금액:{(fv)}, 수익률:{(rate)}%, 원금:{pv}')
#         print(f'{i} 수익:{round(income)}, 총금액:{round(fv)}, 총수익금:{round(fv - originPrice)}, 원금대비 수익률:{round(rate, 2)}%, 원금:{originPrice}, 초기자금대비 수익률:{round(finalRate, 2)}%')



def calculate(pv, r, n, s):
    originPrice = pv
    newpv = pv
    for i in range(1,n+1):
        originPrice += s
        before = newpv
        newpv = newpv + s
        newpv = newpv + (newpv * r)
        fv = newpv
        income = fv - before - s
        rate = (fv - originPrice) / originPrice * 100
        try:
            finalRate = (fv - pv) / pv * 100
        except:
            finalRate = 0
        print(f'{i} 수익:{round(income)}, 총금액:{round(fv)}, 총수익금:{round(fv - originPrice)}, 원금대비 수익률:{round(rate, 2)}%, 원금:{originPrice}, 초기자금대비 수익률:{round(finalRate, 2)}%')


calculate(10000000, 0.2, 10, 12000000)
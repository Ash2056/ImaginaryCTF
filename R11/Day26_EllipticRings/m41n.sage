FLAG = b'ictf{H4xx3d by 7h3 9r347 __Xx_An0nym0u5_xX__}'

def magic_function_to_compute_curve_order(E):
    # This holds because E(Z/p^k Z) ~= E(Z/pZ) × Z/p^k-1 Z
    # The above can be generalized when considering a decomposition of a ring into a product of maximal ideals
    return (E/GF(E.base_ring().characteristic())).order() * E.base_ring().order() // E.base_ring().characteristic()
    # Scary maths

def gen_curve():
    p = random_prime(2^64 - 1, lbound = 2^63) # 64 bits primes rock
    R = Zmod(p^randint(3,5))
    while True:
        a, b = R.random_element(), R.random_element()
        # What the hell is this black magic
        if (4*a^3 + 27*b^2).is_unit(): # Ensure curve is non-singular
            E = EllipticCurve(R, [a, b])
            return p, E, magic_function_to_compute_curve_order(E)

def gen_point(p, E):
    s = E.base_ring().random_element()
    # While true everywhere what a bad coder lol
    while True:
        s += 1
        try:
            return E.lift_x(3*s)
        except:
            pass

def m41n():
    p, E, o = gen_curve()
    P = gen_point(p, E)
    Q = 2*P
    print('P:', P)
    print('Q:', Q)
    flag = int.from_bytes(FLAG, 'big')
    print('Flag:', (flag ^^ (o^3)) & (2^(flag.bit_length() + 1) - 1))

# Salvaged Information
# P: (13721191374366420180377253776387076000480246815852205697410286316623904707509 : 15546216794218269665387064067426591325783663330332949666584538995755179084261 : 1)
# Q:  (7759521132309061296716250650979510027373452958739669671394739010159270474311 : 14302246045604117731126501528071886365994126908953754994206730761987730092254 : 1)
# Flag: 1908238427445950804337450504869547077117085157723645071010868264470221173655056956

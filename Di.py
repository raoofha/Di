''''; xterm-send "echo -ne \"\\033c\"; systemd-run --scope -p MemoryMax=2G --user python3 $0" ; exit 1 ; 
'''
''''; xterm-send "echo -ne \"\\033c\"; python3 $0" ; exit 1 ; 
'''

def di(*args):
  args_l = len(args)
  def product(*iterables, repeat=1):
    pools = [tuple(pool) for pool in iterables] * repeat
    result = [[]]
    for pool in pools: result = [x+[y] for x in result for y in pool]
    return result

  def createPolynomial(n,d,c,x):
    if type(n) != int: return [1]
    if type(d) != int: return [1]
    for cc in c:
      if type(cc) != int: return [1]
    for xx in x:
      if type(xx) != int: return [1]
    n = abs(n)
    d = abs(d)
    m = []
    ds = list(map(lambda i: list(reversed(i)),list(product(range(d+1), repeat=n))))
    #print(ds)
    m = 1
    c_l = len(c)
    x_l = len(x)
    new_c = [0] * (d+1)
    for k,d in enumerate(ds):
      m = c[k] if k<c_l else 0
      for i in range(1,n):
        if i < x_l:
          m *= x[i]**d[i]
        else:
          m = 0
      if d:
        new_c[d[0]] += m
    return new_c

  def divisors(n):
    n = abs(n)
    divs = []
    #for i in range(1, n + 1):
    #  if n % i == 0:
    #    divs.append(-i)
    divs.append(0)
    for i in range(1, n + 1):
      if n % i == 0:
        divs.append(i)
    return divs

  def evaluatePolynomial(coeffs, x):
    result = 0
    degree = 0
    for coef in coeffs:
      result += coef * (x ** degree)
      degree += 1
    return result

  def root(*coeffs):
    constant_term = coeffs[0] if len(coeffs)!=0 else 0
    possible_roots = divisors(constant_term)
    integer_roots = []
    for r in possible_roots:
      if evaluatePolynomial(coeffs, r) == 0:
        integer_roots.append(r)
    return min(integer_roots) if integer_roots else 0 # this is where the magic happens

  def f(*xs): return root(*createPolynomial(args[0] if args_l > 0 else 0,args[1] if args_l > 1 else 0,args[2:],[0]+list(xs)))

  return f

Add = lambda a,b: di(3,1,0,1,-1,0,-1)(a,b) # y-a-b = 0
Mul = lambda a,b: di(3,1,0,1,0,0,0,0,-1,0)(a,b) # y-a*b = 0
Tsub = lambda a,b: di(3,1,0,1,-1,0, 1)(a,b) # y-a+b = 0
Idiv = lambda a,b: di(3,1,0,0,-1,0,0,1,0,0)(a,b) # b*y-a = 0

Not = lambda a: Tsub(1,a)
IsNonZero = lambda a: Not(a)
IsZero = lambda a: IsNonZero(IsNonZero(a))
And = lambda a,b: IsZero(Add(IsZero(a),IsZero(b)))
Or = lambda a,b: IsZero(Mul(a,b))
If = lambda a,b,c: Add(Mul(IsNonZero(a),b),Mul(IsZero(a),c))
Eq = lambda a,b: And(Tsub(a,b),Tsub(b,a))
NotEq = lambda a,b: Not(Eq(a,b))
Lte = lambda a,b: IsZero(Tsub(a,b))
Lt = lambda a,b: And(Lte(a,b),NotEq(a,b))
Gt = lambda a,b: Not(Lte(a,b))
Gte = lambda a,b: Not(Lt(a,b))

Min = lambda a,b: If(Lt(a,b),a,b)
Max = lambda a,b: If(Lt(a,b),b,a)

test = lambda a,b: [(print(f'\x1b[31m{a}\x1b[0m', "==" ,x, f'\x1b[31m{b}\x1b[0m') if str(x)!=str(b) else 0) if b!=None else print(a,"==",x) for x in [eval(a)]]

TRUE = 0
FALSE = 1

test("Not(0)",FALSE)
test("Not(1)",TRUE)
test("Not(2)",TRUE)
test("Not(3)",TRUE)
test("IsZero(0)",TRUE)
test("IsZero(1)",FALSE)
test("IsZero(2)",FALSE)
test("IsZero(3)",FALSE)
test("IsNonZero(0)",FALSE)
test("IsNonZero(1)",TRUE)
test("IsNonZero(2)",TRUE)
test("IsNonZero(3)",TRUE)
test("Or(0,0)",TRUE)
test("Or(1,0)",TRUE)
test("Or(0,1)",TRUE)
test("Or(1,1)",FALSE)
test("Or(42,0)",TRUE)
test("Or(0,42)",TRUE)
test("Or(42,42)",FALSE)
test("And(0,0)",TRUE)
test("And(1,0)",FALSE)
test("And(0,1)",FALSE)
test("And(1,1)",FALSE)
test("And(42,0)",FALSE)
test("And(0,42)",FALSE)
test("And(42,42)",FALSE)
test("Eq(0,0)",TRUE)
test("Eq(1,1)",TRUE)
test("Eq(4,4)",TRUE)
test("Eq(2,4)",FALSE)
test("Eq(4,2)",FALSE)
test("Gte(0,0)",TRUE)
test("Gte(1,0)",TRUE)
test("Gte(2,0)",TRUE)
test("Gte(42,0)",TRUE)
test("Gte(42,41)",TRUE)
test("Gte(42,40)",TRUE)
test("Gte(40,42)",FALSE)
test("Gte(0,42)",FALSE)
test("Gte(0,1)",FALSE)
test("Gt(0,0)",FALSE)
test("Gt(1,0)",TRUE)
test("Gt(2,0)",TRUE)
test("Gt(42,0)",TRUE)
test("Gt(42,41)",TRUE)
test("Gt(42,40)",TRUE)
test("Gt(40,42)",FALSE)
test("Gt(0,42)",FALSE)
test("Gt(0,1)",FALSE)
test("Lt(0,0)",FALSE)
test("Lt(1,1)",FALSE)
test("Lt(2,2)",FALSE)
test("Lt(4,2)",FALSE)
test("Lt(2,4)",TRUE)
test("Lte(0,0)",TRUE)
test("Lte(1,1)",TRUE)
test("Lte(2,2)",TRUE)
test("Lte(4,2)",FALSE)
test("Lte(2,4)",TRUE)
test("NotEq(0,0)",FALSE)
test("NotEq(1,1)",FALSE)
test("NotEq(4,4)",FALSE)
test("NotEq(2,4)",TRUE)
test("NotEq(4,2)",TRUE)
test("Add(2,2)",4)
test("Add(2,0)",2)
test("Add(10,10)",20)
test("Add(33,11)",44)
test("Tsub(2,2)",0)
test("Tsub(10,10)",0)
test("Tsub(33,11)",22)
test("Tsub(2,4)",0)
test("Mul(2,4)",8)
test("Mul(10,10)",100)
test("Mul(0,4)",0)
test("Mul(42,0)",0)
test("Idiv(43,42)",0)
test("Idiv(42,42)",1)
test("Idiv(4,2)",2)
test("Idiv(5,2)",0)
test("Idiv(2,4)",0)
test("If(0,2,4)",2)
test("If(1,2,4)",4)
test("If(2,2,4)",4)
test("If(42,2,4)",4)
test("Min(42,2)",2)
test("Min(2,42)",2)
test("Min(0,42)",0)
test("Min(42,0)",0)
test("Min(0,0)",0)
test("Max(42,2)",42)
test("Max(2,42)",42)
test("Max(0,42)",42)
test("Max(42,0)",42)
test("Max(0,0)",0)

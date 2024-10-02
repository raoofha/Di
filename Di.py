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
    new_c = [0] * (d+1)
    for k,d in enumerate(ds):
      m = c[k] if k<c_l else 0
      for i in range(1,n):
        m *= x[i]**d[i]
      if d:
        new_c[d[0]] += m
    return new_c

  def divisors(n):
    n = abs(n)
    divs = [0]
    for i in range(1, n + 1):
      if n % i == 0:
        divs.append(i)
        #divs.append(-i)
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

Not = di(2,1,-1,1,1) # -1+y+a=0 
isZero = di(2,1,0,0,-1,1) # -a+a*y=0
Or = di(3,1,0,0,0,0,0,0,-1,1) # -a*b+a*b*y = 0
And = di(3,1,0,0,-1,1,-1,1) # -(a+b)+(a+b)*y = 0 -> -a-b+a*y+b*y = 0
eq = di(3,1,0,0,1,-1,-1,1) # (a-b)*(1-y)=0 -> a-y*a-b+y*b = 0
add = di(3,1,0,1,-1,0,-1) # y-a-b = 0
tsub = di(3,1,0,1,-1,0, 1) # y-a+b = 0
mul = di(3,1,0,1,0,0,0,0,-1,0) # y-a*b = 0

isNonZero = lambda a: Not(a)
If = lambda a,b,c: add(mul(isNonZero(a),b),mul(isZero(a),c))
NotEq = lambda a,b: Not(eq(a,b))
lte = lambda a,b: isZero(tsub(a,b))
lt = lambda a,b: And(lte(a,b),NotEq(a,b))
gt = lambda a,b: Not(lte(a,b))
gte = lambda a,b: Not(lt(a,b))

Min = lambda a,b: If(lt(a,b),a,b)
Max = lambda a,b: If(lt(a,b),b,a)

test = lambda a,b: [(print(f'\x1b[31m{a}\x1b[0m', "==" ,x, f'\x1b[31m{b}\x1b[0m') if str(x)!=str(b) else 0) if b!=None else print(a,"==",x) for x in [eval(a)]]

TRUE = 0
FALSE = 1

test("Not(0)",FALSE)
test("Not(1)",TRUE)
test("Not(2)",TRUE)
test("Not(3)",TRUE)
test("isZero(0)",TRUE)
test("isZero(1)",FALSE)
test("isZero(2)",FALSE)
test("isZero(3)",FALSE)
test("isNonZero(0)",FALSE)
test("isNonZero(1)",TRUE)
test("isNonZero(2)",TRUE)
test("isNonZero(3)",TRUE)
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
test("eq(0,0)",TRUE)
test("eq(1,1)",TRUE)
test("eq(4,4)",TRUE)
test("eq(2,4)",FALSE)
test("eq(4,2)",FALSE)
test("gte(0,0)",TRUE)
test("gte(1,0)",TRUE)
test("gte(2,0)",TRUE)
test("gte(42,0)",TRUE)
test("gte(42,41)",TRUE)
test("gte(42,40)",TRUE)
test("gte(40,42)",FALSE)
test("gte(0,42)",FALSE)
test("gte(0,1)",FALSE)
test("gt(0,0)",FALSE)
test("gt(1,0)",TRUE)
test("gt(2,0)",TRUE)
test("gt(42,0)",TRUE)
test("gt(42,41)",TRUE)
test("gt(42,40)",TRUE)
test("gt(40,42)",FALSE)
test("gt(0,42)",FALSE)
test("gt(0,1)",FALSE)
test("lt(0,0)",FALSE)
test("lt(1,1)",FALSE)
test("lt(2,2)",FALSE)
test("lt(4,2)",FALSE)
test("lt(2,4)",TRUE)
test("lte(0,0)",TRUE)
test("lte(1,1)",TRUE)
test("lte(2,2)",TRUE)
test("lte(4,2)",FALSE)
test("lte(2,4)",TRUE)
test("NotEq(0,0)",FALSE)
test("NotEq(1,1)",FALSE)
test("NotEq(4,4)",FALSE)
test("NotEq(2,4)",TRUE)
test("NotEq(4,2)",TRUE)
test("add(2,2)",4)
test("add(2,0)",2)
test("add(10,10)",20)
test("add(33,11)",44)
test("tsub(2,2)",0)
test("tsub(10,10)",0)
test("tsub(33,11)",22)
test("tsub(2,4)",0)
test("mul(2,4)",8)
test("mul(10,10)",100)
test("mul(0,4)",0)
test("mul(42,0)",0)
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

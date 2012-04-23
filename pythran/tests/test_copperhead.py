from pythran import python_interface
import unittest

class TestBase(unittest.TestCase):

    def run_test(self, code, *params, **interface):
        for name in sorted(interface.keys()):
            mod = python_interface("test_"+name, code, **interface)
            res = getattr(mod,name)(*params)
            print res

# from copperhead test suite
# https://github.com/copperhead
    def test_saxpy(self):
        self.run_test("def saxpy(a, x, y): return map(lambda xi, yi: a * xi + yi, x, y)", 1.5, [1,2,3], [0.,2.,4.], saxpy=("float","int list", "float list"))
    
    def test_saxpy2(self):
        self.run_test("def saxpy2(a, x, y): return [a*xi+yi for xi,yi in zip(x,y)]", 1.5, [1,2,3], [0.,2.,4.], saxpy2=("float","int list", "float list"))

    def test_saxpy3(self):
        code="""
def saxpy3(a, x, y):
    def triad(xi, yi): return a * xi + yi
    return map(triad, x, y)
"""
        self.run_test(code,  1.5, [1,2,3], [0.,2.,4.], saxpy3=("float","int list", "float list"))

    def test_sxpy(self):
        code="""
def sxpy(x, y):
    def duad(xi, yi): return xi + yi
    return map(duad, x, y)
"""
        self.run_test(code,  [1,2,3], [0.,2.,4.], sxpy=("int list", "float list"))
    
    def test_incr(self):
        self.run_test("def incr(x): return map(lambda xi: xi + 1, x)", [0., 0., 0.], incr=("float list"))

    def test_as_ones(self):
        self.run_test("def as_ones(x): return map(lambda xi: 1, x)", [0., 0., 0.], as_ones=("float list"))

    def test_idm(self):
        self.run_test("def idm(x): return map(lambda b: b, x)", [1, 2, 3], idm=("int list"))
    
    def test_incr_list(self):
        self.run_test("def incr_list(x): return [xi + 1 for xi in x]", [1., 2., 3.], incr_list=("float list"))


    def test_idx(self):
        code=""" 
def idx(x):
    def id(xi): return xi
    return map(id, x)"""
        self.run_test(code, [1,2,3], idx=("int list"))
    
    def test_rbf(self):
        code="""
from math import exp
def norm2_diff(x, y):
   def el(xi, yi):
       diff = xi - yi
       return diff * diff
   return sum(map(el, x, y))

def rbf(ngamma, x, y):
   return exp(ngamma * norm2_diff(x,y))"""
        self.run_test(code, 2.3, [1,2,3], [1.1,1.2,1.3], rbf=("float","float list", "float list"))

# from copperhead-new/copperhead/prelude.py
    def test_indices(self):
        self.run_test("def indices(A):return range(len(A))",[1,2], indices=("int list"))

    def test_gather(self):
        self.run_test("def gather(x, indices): return [x[i] for i in indices]", [1,2,3,4,5],[0,2,4], gather=("int list", "int list"))

    def test_scatter(self):
        code="""
def indices(x): return xrange(len(x))
def scatter(src, indices_, dst):
    assert len(src)==len(indices_)
    result = list(dst)
    for i in xrange(len(src)):
        result[indices_[i]] = src[i]
    return result
"""
        self.run_test(code, [0.0,1.0,2.,3,4,5,6,7,8,9],[5,6,7,8,9,0,1,2,3,4],[0,0,0,0,0,0,0,0,0,0,18], scatter=("float list", "int list", "float list"))

    def test_scan(self):
        code="""
def prefix(A): return scan(lambda x,y:x+y, A)
def scan(f, A):
    B = list(A)
    for i in xrange(1, len(B)):
        B[i] = f(B[i-1], B[i])
    return B
"""
        self.run_test(code, [1,2,3], prefix=("float list"))
        


# from Copperhead: Compiling an Embedded Data Parallel Language
# by Bryan Catanzaro, Michael Garland and Kurt Keutzer
# http://www.eecs.berkeley.edu/Pubs/TechRpts/2010/EECS-2010-124.html
#def spvv_csr(x, cols, y):
#    """
#    Multiply a sparse row vector x -- whose non-zero values are in the
#    specified columns -- with a dense column vector y.
#    """
#    z = gather(y, cols)
#    return sum(map(lambda a, b: a * b, x, z))
# 
#def spmv_csr(Ax, Aj, x):
#    """
#    Compute y = Ax for CSR matrix A and dense vector x.
# 
#    Ax and Aj are nested sequences where Ax[i] are the non-zero entries
#    for row i and Aj[i] are the corresponding column indices.
#    """
#    return map(lambda y, cols: spvv_csr(y, cols, x), Ax, Aj)
#
#def spmv_ell(data, idx, x):
#    def kernel(i):
#        return sum(map(lambda Aj, J: Aj[i] * x[J[i]], data, idx))
#    return map(kernel, indices(x))
#
#    @cu
#    def vadd(x, y):
#    return map(lambda a, b: return a + b, x, y)
#    @cu
#    def vmul(x, y):
#    return map(lambda a, b: return a * b, x, y)
#    @cu
#    def form_preconditioner(a, b, c):
#    def det_inverse(ai, bi, ci):
#    return 1.0/(ai * ci - bi * bi)
#    indets = map(det_inverse, a, b, c)
#    p_a = vmul(indets, c)
#    p_b = map(lambda a, b: -a * b, indets, b)
#    p_c = vmul(indets, a)
#    return p_a, p_b, p_c
#    @cu
#    def precondition(u, v, p_a, p_b, p_c):
#    e = vadd(vmul(p_a, u), vmul(p_b, v))
#    f = vadd(vmul(p_b, u), vmul(p_c, v))
#    return e, f


        

if __name__ == '__main__':
        unittest.main()

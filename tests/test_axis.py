from duneglider.f_utils.axis import *

def test_na():
    npa = na([1, 2, 3])
    assert (npa == np.array([[1, 2, 3]])).all()

def test_nat():
    npat = nat([1, 2, 3])
    assert (npat == np.array([[1], [2], [3]])).all()

def test_Rbti():
    Xi = Rbti(nat([[1, 0, 0]]), nat([0, 45*np.pi/180, 0]))
    assert (Xi == np.array([[ 0.70710678], [ 0 ], [-0.70710678]])).all
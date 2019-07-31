#------------------------------------------------------
# Module : Bond Counting
# Description : Stuff for the bound counting scheme
#------------------------------------------------------

# Dictionnaries for the bound counting scheme
n1 = {
'niA' : 4,
'niE' : [2,3,5,6],
'nfA' : 7,
'nfE' : [2,6,8,18]
 }
n2 = {
'niA' : 5,
'niE' : [1,3,4,6],
'nfA' : 9,
'nfE' : [1,3,8,10]
}
n3 = {
'niA' : 6,
'niE' : [1,2,4,5],
'nfA' : 11,
'nfE' : [2,4,10,12]
}
n4 = {
'niA' : 1,
'niE' : [2,3,5,6],
'nfA' : 13,
'nfE' : [3,5,12,14]
}
n5 = {
'niA' : 2,
'niE' : [1,3,4,6],
'nfA' : 15,
'nfE' : [4,6,14,16]
}
n6 = {
'niA' : 3,
'niE' : [1,2,4,5],
'nfA' : 17,
'nfE' : [1,5,16,18]
}

# List of the dictionnaries for the bound counting scheme
bond_dicts = [0,n1,n2,n3,n4,n5,n6]

# Function for the bound counting scheme
def theta(x):
    T = 0
    if x > 0:
        T = 1
    return T

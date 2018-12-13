# Remove Revision
Script uses `pandas IO` and `strategy pattern`. Script remove revision from csv file.

### Example
#### Input
MNOPQYS1286101/1R1D-TTT <br />
QRST-085594B.351 <br />
QRST-086019A.307-TTT <br />
QRST-472927A.203-HHHH <br />
ABCD-55-990079-04-A0-5112537 <br />
ABCD-55-990102-02-A0 <br />
QRST-087732A.308 <br />
QRST-472181A.344 <br />
ABCD-55-990117-01-C0 <br />
QRST-472573A.344-INF-LOW <br />
ABCD-55-990074-01-D0-BBB <br />
ABCD-55-990108-02-D0-EA645

#### Output
MNOPQYS1286101/1 <br />
QRST-085594B <br />
QRST-086019A <br />
QRST-472927A <br />
ABCD-55-990079 <br />
ABCD-55-990102 <br />
QRST-087732A <br />
QRST-472181A <br />
ABCD-55-990117 <br />
QRST-472573A <br />
ABCD-55-990074 <br />
ABCD-55-990108

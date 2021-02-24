import DualMomentum

dm = DualMomentum.DualMomentum()
rm = dm.get_rltv_momentum('2019-05-15', '2019-08-15', 10)
dm.get_abs_momentum(rm, '2019-08-15', '2019-11-15')
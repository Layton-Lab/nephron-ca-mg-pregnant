from values import *

def NCC(cell,i,memb_id,xNCC,area):


	# Effect of CaSR (inhibition)
	alpha_ncc = 0.5
	EC_50_Ca = 1.25
	EC_50_Mg = 2.5

	xNCC = xNCC *  (1 + alpha_ncc * (cell.conc[15, 0] ** 4) / (cell.conc[15, 0] ** 4 + EC_50_Ca ** 4)) * \
                                    (1 + 0.4 * alpha_ncc * (cell.conc[16, 0] ** 4) / (
                                                cell.conc[16, 0] ** 4 + EC_50_Mg ** 4))


	if cell.segment == 'DCT':
		LzD=i-1
		x1=LzD+1
		xn=cell.total
		xdct2=2.0/3.0

		if x1/xn<xdct2:
			NCCexp=1.0
		else:
			NCCexp=2*(1-(x1/xn-xdct2)/(1-xdct2))
	else:
		NCCexp = 1.0
	alp=cell.conc[0,memb_id[0]]/dKnncc
	alpp=cell.conc[0,memb_id[1]]/dKnncc
	betp=cell.conc[2,memb_id[0]]/dKcncc
	betpp=cell.conc[2,memb_id[1]]/dKcncc

	gamp=cell.conc[0,memb_id[0]]*cell.conc[2,memb_id[0]]/(dKnncc*dKncncc)
	gampp=cell.conc[0,memb_id[1]]*cell.conc[2,memb_id[1]]/(dKnncc*dKncncc)

	rhop=1+alp+betp+gamp
	rhopp=1+alpp+betpp+gampp

	sigma=rhop*(poppncc+gampp*pnppncc)+rhopp*(popncc+gamp*pnpncc)
	dJNCC=NCCexp*cell.area[memb_id[0],memb_id[1]]*xNCC*pnpncc*poppncc*(gamp-gampp)/sigma

	return [0,2],[dJNCC,dJNCC]
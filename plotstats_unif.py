from pyx import *
from math import pi

text.set(mode='latex')
unit.set(wscale=1.5, xscale=1.2)
figwidth = 10
figheight = figwidth/1.618
margin = 0.5


runtab = [
    ['unif-weak-256', 1, 1000 ],
#     ['unif-weak-zerob-256', 1, 400 ],
    ]


datadir = '.'
istep = 1
tmax = 1000

for runid, i1, i2 in runtab:
    statsfile = '%s/%s-%4.4i-%4.4i-%4.4i.stats' % (datadir, runid, i1, i2, istep)
    vstatsfile = '%s/%s-%4.4i-%4.4i-%4.4i.vstats' % (datadir, runid, i1, i2, istep)
    rstatsfile = '%s/%s-%4.4i-%4.4i-%4.4i.rstats' % (datadir, runid, i1, i2, istep)
    dstatsfile = '%s/%s-%4.4i-%4.4i-%4.4i.dstats' % (datadir, runid, i1, i2, istep)

    mylines = graph.style.line()

    ## Graph 1 : density, clumping

    c = canvas.canvas()

    ##
    ## Mean density
    ##
    d = []

    for Dmean, title in [ 
	('Dmean_i', r'$\langle n\rangle_\mathrm{ion}$'),
	('Dmean_n', r'$\langle n\rangle_\mathrm{neut}$'), 
	('Dmean_tot', r'$\langle n\rangle_\mathrm{tot}$'), 
	]:
	d.append(graph.data.file(dstatsfile, x='Time', y=Dmean, title=title))

    g = graph.graphxy(width=figwidth, height=figheight, 
    # 		  x=graph.axis.linear(title='Time, 1000~yr'), 
		      x=graph.axis.linear(min=0, max=tmax, painter=graph.axis.painter.linked()),
		      y=graph.axis.logarithmic(min=5, max=5.e5,
					  title=r'Mean densities, cm$^{-3}$'),
		      key=graph.key.key(pos='tr', textattrs=[trafo.scale(0.7)])
		      )
    g.plot(d, [graph.style.line()])

    c.insert(g, [trafo.translate(0, figheight+margin)])

    ##
    ## Clumping 
    ##
    d = []
    for Clump, title in [ 
			  ('D2mean_i/Dmean_i**2', r'$C_\mathrm{ion}$'),
			  ('D2mean_n/Dmean_n**2', r'$C_\mathrm{neut}$'), 
			  ('D3mean_i**2/D2mean_i**3', r'$\varepsilon_\mathrm{ion}^{-1}$')]:
	d.append(graph.data.file(dstatsfile, x='Time', y=Clump, title=title))

	g = graph.graphxy(width=figwidth, height=figheight, 
			  x=graph.axis.linear(min=0, max=tmax, title='Time, 1000~yr'), 
			  y=graph.axis.logarithmic(title=r'Degree of clumping',
    # 	    r'Clumping factor, $C = \langle n^2 \rangle / \langle n \rangle^2$',
						   min=0.9, max=450
		),
		      key=graph.key.key(pos='tr', textattrs=[trafo.scale(0.7)])
		      )

    g.plot(d, [mylines])

    g.writePDFfile('clumping_vs_t_' + runid)

    c.insert(g)

    c.writePDFfile('densities_vs_t_' + runid)


    ## Graph 2 : ion frac, radius

    c = canvas.canvas()

    ##
    ## Ion frac
    ##
#     d = []

#     for Frac, title in [ ('Ifrac_v2', r'$X_\mathrm{vol}$'), 
# 			 ('Ifrac_m', r'$X_\mathrm{mass}$') ]:
# 	d.append(graph.data.file(statsfile, x='Time', y=Frac, title=title))

#     g = graph.graphxy(width=figwidth, height=figheight, 
#     # 		  x=graph.axis.linear(title='Time, 1000~yr'), 
# 		      x=graph.axis.linear(min=0, max=tmax, painter=graph.axis.painter.linked()),
# 		      y=graph.axis.logarithmic(min=1.e-6, max=1, title=r'Total ionized fraction'),
# 		      key=graph.key.key(pos='tl', textattrs=[trafo.scale(0.7)])
# 		      )

#     g.plot(d, [graph.style.line()])

#     c.insert(g, [trafo.translate(0, figheight+margin)])


    ##

    ##
    ## Radius
    ##
    d = []
    d.append(graph.data.file(rstatsfile, x='Time', y='rx2/3.085677582e18', 
#     d.append(graph.data.file(rstatsfile, x='Time', y='rx1/3.086e18', 
			     title=r"$\left\langle R_\mathrm{ion}\right\rangle$"
			     ))
    d.append(graph.data.file(rstatsfile, x='Time', y='rif_min*4.0/256', 
			     title=r"$R_\mathrm{min}$"
			     ))
    d.append(graph.data.file(rstatsfile, x='Time', y='rif_max*4.0/256', 
			     title=r"$R_\mathrm{max}$"
			     ))
    # d.append(graph.data.file(rstatsfile, x='Time', y='rmean_mass_i/3.086e18',
    # 			 title=r"$\left\langle R\right\rangle_\mathrm{ion}$"
    # 			 ))

    g = graph.graphxy(width=figwidth, height=figheight, 
		      x=graph.axis.linear(min=0, max=tmax, title='Time, 1000~yr'), 
		      y=graph.axis.linear(min=0, max=2,
					  title=r'Mean radius, parsec'),
		      key=graph.key.key(pos='tl', textattrs=[trafo.scale(0.7)],
					hdist=0.3*unit.v_cm)
		      )

    # homogeneous solution
    # Where does this come from?
    # R = R_0 (1 + 7 c_i t / 4 R_0)**4/7
    # R_0 = (3 Q_H / 4 pi alpha n^2 )^1/3
    #
    # For the weak runs, we have Q_H = 5.e46 instead of 5.e48
    # Also,  <T> is less: more like 8300 K (why?)
    #
    # Q_H = 5.e48 : R_0 = 0.539 pc with T=10^4 or 0.520 pc with T=9000
    # Q_H = 5.e46 : R_0 = 0.116 pc with T=10^4 or 0.109 pc with T=8300
    #
    # rho c_i^2 = (1 + y_e) n k T => c_i = sqrt( (1 + y_e) k T / m )
    #
    # m = 1.3 mp, T = 8300 K, y_e = 1 => c_i = 1.027e6 cm/s (10.27 km/s)
    #
    # t_0 = 4 R_0 / 7 c_i = 54.4 (R_0 / pc) kyr
    # 
    # Actually, the above isn't quite right - best do it directly in python
    # Run parameters
    QH = 5.e46
#     Tmean = 8400.0
    Tmean = 8900.0		# this gives the best fit to unif-weak-zerob256
    n = 1000.0
    xi = 1.0
    # physical constants
    k = 1.3806503e-16
    pc = 3.085677582e18
    kyr = 1000.*3.15576e7
    m = 1.3*1.67262158e-24
    # This is taken from Garrelt's cgsconstants.f90
    alpha = 2.59e-13*(Tmean/1.e4)**-0.7
    # Find characteristic radius and time
    R0 = (3*QH / (4*pi*alpha*n**2) )**(1./3.)
    ci = ( (1.0+xi)*k*Tmean / m)**0.5
    t0 = 4.*R0/(7.*ci) 
    # Put in right units
    R0 = R0 / pc
    t0 = t0 / kyr
    print "R0 = %.2f pc, t0 = %.2f kyr" % (R0, t0)
    f = graph.data.function(
	"y(x) = R0*(1.0 + x/t0)**(4./7.)", 
	context=locals(),
	title=r"$R_\mathrm{Str\ddot om}$"
    )
    g.plot(f, [graph.style.line([color.gray(0.8), style.linewidth.THIck])])
    # plot the simulation lines last since they are thinner
    g.plot(d, [graph.style.line()])

    c.insert(g)

    g = graph.graphxy(width=figwidth, height=figheight, 
 		      x=graph.axis.linear(min=0, max=tmax, painter=graph.axis.painter.linked()),
		      y=graph.axis.linear(#min=0, max=0.01,
					  title=r'Relative error: \(\left(\left\langle R_\mathrm{ion}\right\rangle - R_\mathrm{Str\ddot om}\right)/R_\mathrm{Str\ddot om}\)'),
		      key=None)
    d = graph.data.file(rstatsfile, x='Time', 
			y='((rx2/pc) - R0*(1.0 + Time/t0)**(4./7.))/(R0*(1.0 + Time/t0)**(4./7.))',
			context=locals(),
			title=None
			)
    g.plot(d, [graph.style.line()])
    c.insert(g, [trafo.translate(0, figheight+margin)])


    c.writePDFfile('radii_vs_t_' + runid)

    ##
    ## RMS and mean radial velocities
    ##
    d = []

    km = 1.e5

    for Vel, title in [ 
			 ('Vrms_vol_i', 
			  r'$\left\langle v^2\right\rangle_\mathrm{ion}^{1/2}$'),
			 ('Vrms_vol_n', 
			  r'$\left\langle v^2\right\rangle_\mathrm{neut}^{1/2}$'), 
			 ]:
	d.append(graph.data.file(statsfile, x='Time', y=Vel+'/km', title=title, context=locals()))

    for Vel, title in [ 
			 ('Vr_vol_i', r'$\left\langle v_r\right\rangle_\mathrm{ion}$'),
			 ('Vr_vol_n', r'$\left\langle v_r\right\rangle_\mathrm{neut}$'), 
			 ]:
	d.append(graph.data.file(vstatsfile, x='Time', y=Vel+'/km', title=title, context=locals()))


    g = graph.graphxy(width=figwidth, height=figwidth,
		      x=graph.axis.linear(min=0, max=tmax, title='Time, 1000~yr'), 
		      y=graph.axis.linear(min=0, max=6.5,
					  title=r'Mean gas velocities, km~s$^{-1}$'),
		      key=graph.key.key(pos='tr', textattrs=[trafo.scale(0.7)])
		      )

    g.plot(d, [graph.style.line()])

    # homogeneous solution
    # 
    # V = (3/8) c_i (1 + 7 c_i t / 4 R_0)**-3/7
    f = graph.data.function(
	"y(x) = (3./8.)*11.6*(1.0 + x/t0)**(-3./7.)",
	context=locals(),
	title=r'$\left\langle v_r\right\rangle_\mathrm{Str\ddot om}$')
    g.plot(f, [graph.style.line([color.gray(0.8), style.linewidth.Thick])])

    g.writePDFfile('velocities_vs_t_' + runid)




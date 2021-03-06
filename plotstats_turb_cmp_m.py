from pyx import *
from math import pi

text.set(mode='latex')
text.preamble(r"\usepackage[varg]{txfonts}")
unit.set(wscale=1.5, xscale=1.2)
figwidth = 10
figheight = figwidth/1.618
margin = 0.5

# This version puts the magnetic and non-magnetic on the same graph

runtab = [
    [5.e48, 'Ostar', ['Ostar-et', 'Ostar-HD'], 5, [400, 355], 5, 400],
    [5.e46, 'Bstar', ['Bstar-ep', 'Bstar-HDep'], 10, [1370, 1450], 10, 1500],
    ]


datadir = '.'
every = 10

transparency = color.transparency(0.3)
symbol = graph.style.symbol(graph.style.symbol.square, 0.1, [deco.filled, transparency])

linestyles_HD = [style.linewidth.normal, transparency]
linestyles_MHD = [style.linewidth.normal, transparency]
linestyles = [linestyles_HD, linestyles_MHD]
keyscale = trafo.scale(0.9)

for QH, starid, runids, i1, i2s, istep, tmax in runtab:
    print "Creating stats graph for %s star" % starid
    statsfiles = []
    vstatsfiles = []
    rstatsfiles = []
    dstatsfiles = []

    for runid, i2 in zip(runids, i2s):
	statsfiles.append('%s/%s-%4.4i-%4.4i-%4.4i.stats' % (datadir, runid, i1, i2, istep)) 
	vstatsfiles.append('%s/%s-%4.4i-%4.4i-%4.4i.vstats' % (datadir, runid, i1, i2, istep)) 
	rstatsfiles.append('%s/%s-%4.4i-%4.4i-%4.4i.rstats' % (datadir, runid, i1, i2, istep)) 
	dstatsfiles.append('%s/%s-%4.4i-%4.4i-%4.4i.dstats' % (datadir, runid, i1, i2, istep)) 


    ## Graph 1 : densities

    c = canvas.canvas()

    ##
    ## Mean density
    ##
    g = graph.graphxy(width=figwidth, height=figheight, 
		      x=graph.axis.linear(min=0, max=tmax, title='Time, 1000~yr'), 
		      y=graph.axis.logarithmic(min=5, max=5.e5,
					  title=r'Mean densities, cm$^{-3}$'),
		      key=graph.key.key(pos='tr', textattrs=[keyscale])
		      )
    for i in 0, 1:
	d = []; dd = [] 
	for Dmean, title in [ 
	    ('Dmean_i', r'Ionized'),
	    ('Dmean_n', r'Neutral'), 
	    ('Dmean_m', r'Molecular'), 
	    ]:
	    if i == 1 : title = None
	    d.append(graph.data.file(dstatsfiles[i], x='Time', y=Dmean, title=title))
	    dd.append(graph.data.file(dstatsfiles[i], x='Time', y=Dmean, title=None, every=every))
	g.plot(d, [graph.style.line(linestyles[i])])
	if i==0: g.plot(dd, [symbol])

    c.insert(g)

    c.writePDFfile('comparison1_vs_t_' + starid)


    ## Graph 2 : ion frac, radius

    c = canvas.canvas()

    ##
    ## Ion frac
    ##
    g = graph.graphxy(width=figwidth, height=figheight, 
		      x=graph.axis.linear(min=0, max=tmax, painter=graph.axis.painter.linked()),
		      y=graph.axis.logarithmic(min=1.e-6, max=1, title=r'Ionized fraction'),
		      key=graph.key.key(pos='br', textattrs=[keyscale])
		      )

    for i in 0, 1:
	d = []; dd = []
	for Frac, title in [ ('Ifrac_v2', r'Volume'), 
			     ('Ifrac_m', r'Mass') ]:
	    if i == 1 : title = None
	    d.append(graph.data.file(statsfiles[i], x='Time', y=Frac, title=title))
	    dd.append(graph.data.file(statsfiles[i], every=every, x='Time', y=Frac, title=None))
	    
	g.plot(d, [graph.style.line(linestyles[i])])
	if i == 0: g.plot(dd, [symbol])
    c.insert(g, [trafo.translate(0, 2*(figheight+margin))])


    ##
    ## Neutral frac
    ##
    g = graph.graphxy(width=figwidth, height=figheight, 
		      x=graph.axis.linear(min=0, max=tmax, painter=graph.axis.painter.linked()),
		      y=graph.axis.linear(min=0, max=1, title=r'Neutral fraction'),
		      key=graph.key.key(pos='tr', textattrs=[keyscale])
		      )

    for i in 0, 1:
	d = []; dd = []
	for Frac, title in [ ('Nfrac_v', r'Volume'), 
			     ('Nfrac_m', r'Mass') ]:
	    if i == 1 : title = None
	    d.append(graph.data.file(statsfiles[i], x='Time', y=Frac, title=title))
	    dd.append(graph.data.file(statsfiles[i], every=every, x='Time', y=Frac, title=None))
	    
	g.plot(d, [graph.style.line(linestyles[i])])
	if i == 0: g.plot(dd, [symbol])
    c.insert(g, [trafo.translate(0, figheight+margin)])

    ##
    ## Molecular frac
    ##
    g = graph.graphxy(width=figwidth, height=figheight, 
		      x=graph.axis.linear(min=0, max=tmax, title='Time, 1000~yr'),
		      y=graph.axis.linear(min=0, max=1, title=r'Molecular fraction'),
		      key=graph.key.key(pos='tr', textattrs=[keyscale])
		      )

    for i in 0, 1:
	d = []; dd = []
	for Frac, title in [ ('Mfrac_v', r'Volume'), 
			     ('Mfrac_m', r'Mass') ]:
	    if i == 1 : title = None
	    d.append(graph.data.file(statsfiles[i], x='Time', y=Frac, title=title))
	    dd.append(graph.data.file(statsfiles[i], every=every, x='Time', y=Frac, title=None))
	    
	g.plot(d, [graph.style.line(linestyles[i])])
	if i == 0: g.plot(dd, [symbol])
    c.insert(g)

    c.writePDFfile('comparison2_vs_t_' + starid)

    ##

    ## Graph 2b : radius

    c = canvas.canvas()
    ##
    ## Radius
    ##
    g = graph.graphxy(width=figwidth, height=figheight, 
		      x=graph.axis.linear(min=0, max=tmax, title='Time, 1000~yr'), 
		      y=graph.axis.linear(min=0, max=2.5,
					  title=r'Radius, parsec'),
		      key=graph.key.key(pos='tl', textattrs=[keyscale],
					hdist=0.3*unit.v_cm)
		      )
	       

    for i in 0, 1:
	d = []; dd = []
	d.append(graph.data.file(rstatsfiles[i], x='Time', y='rx2/3.086e18', 
				 title=[r"$\left\langle R_\mathrm{ion}\right\rangle$", None][i]
				 ))
	d.append(graph.data.file(rstatsfiles[i], x='Time', y='rif_min*4.0/256', 
				 title=[r"$R_\mathrm{min}$", None][i]
				 ))
	d.append(graph.data.file(rstatsfiles[i], x='Time', y='rif_max*4.0/256', 
				 title=[r"$R_\mathrm{max}$", None][i]
				 ))
	dd.append(graph.data.file(rstatsfiles[i], x='Time', y='rx2/3.086e18', 
				 title=None, every=every
				 ))
	dd.append(graph.data.file(rstatsfiles[i], x='Time', y='rif_min*4.0/256', 
				 title=None, every=every
				 ))
	dd.append(graph.data.file(rstatsfiles[i], x='Time', y='rif_max*4.0/256', 
				 title=None, every=every
				 ))
	g.plot(d, [graph.style.line(linestyles[i])])
	if i == 0: g.plot(dd, [symbol])

    # homogeneous solution
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
	title=r"$R_\mathrm{Spitzer}$"
    )
#     f = graph.data.function(
# 	"y(x) = 0.532*(1.0 + 0.0390*x)**(4./7.)", 
# 	title=r"$R_\mathrm{Spitzer}$"
#     )
    g.plot(f, [graph.style.line([color.transparency(0.8), style.linewidth.THIck])])

    c.insert(g)

    c.writePDFfile('comparison2b_vs_t_' + starid)

    ##
    ## RMS and mean radial velocities
    ##

    c = canvas.canvas()

    km = 1.e5

    yshift = 0
    for id, longid, vmin, vmax, pos in [
        ["m", "mol", -2, 5, {'Bstar': 'tl', 'Ostar': 'tl'}], 
        ["n", "neut", -1, 6, {'Bstar': 'tl', 'Ostar': 'mr'}], 
        ["i", "ion", -1, 13, {'Bstar': 'tr', 'Ostar': 'tr'}], 
        ]:
        thisfigheight = figwidth*(vmax - vmin)/14.0
        if yshift == 0:
            xpainter = graph.axis.painter.regular()
        else:
            xpainter = graph.axis.painter.linked()

        g = graph.graphxy(width=figwidth, height=thisfigheight,
                          x=graph.axis.linear(min=0, max=tmax, title='Time, 1000~yr', painter=xpainter), 
                          y=graph.axis.linear(min=vmin, max=vmax,
                                              title=r'Mean gas velocities, km~s$^{-1}$'),
                          key=graph.key.key(pos=pos[starid], textattrs=[keyscale])
                          )
        for i in 0, 1:
            d = []; dd = []
            for Vel, title, thisfile in [ 
                ['Vrms_vol_%s'% (id), 
                 r'$\left\langle v^2\right\rangle_\mathrm{%s}^{1/2}$' % (longid),
                 statsfiles[i]
                 ],
                ['Vr_vol_%s' % (id), 
                 r'$\left\langle v_r\right\rangle_\mathrm{%s}$' % (longid),
                 vstatsfiles[i]
                 ],
                ]:
                if i == 1 : title = None
                d.append(graph.data.file(thisfile, x='Time', y=Vel+'/km', title=title, context=locals()))
                dd.append(graph.data.file(thisfile, every=every, x='Time', y=Vel+'/km', title=None, context=locals()))

            g.plot(d, [graph.style.line(linestyles[i])])
            if i==0: g.plot(dd, [symbol])

        if longid == "ion":
            # homogeneous solution
            # 
            # V = (3/8) c_i (1 + 7 c_i t / 4 R_0)**-3/7
            f = graph.data.function(
                "y(x) = (3./8.)*11.6*(1.0 + x/t0)**(-3./7.)",
                context=locals(),
                title=r'$\left\langle v_r\right\rangle_\mathrm{Spitzer}$')
            g.plot(f, [graph.style.line([color.transparency(0.8), style.linewidth.THIck])])

        # insert zero line
        g.stroke(g.ygridpath(0), [style.linewidth.thin])
        c.insert(g, [trafo.translate(0, yshift)])
        yshift += thisfigheight+margin

    c.writePDFfile('comparison3_vs_t_' + starid)




def plot_graph(dt = 1.0):
    t = [0.0] # time
    x_var, y_var, z_var = magnotometer() # mag
    x = [x_var]
    y = [y_var]
    z = [z_var]

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    xline, = ax.plot(t, x, 'r-')
    yline, = ax.plot(t, y, 'g-')
    zline, = ax.plot(t, z, 'b-')

    while True:
        t.append(t[-1] + dt)
        x_var, y_var, z_var = magnotometer() # mag
        x.append(x_var)
        y.append(y_var)
        z.append(z_var)

        xline.set_xdata(t)
        yline.set_xdata(t)
        zline.set_xdata(t)

        xline.set_ydata(x)
        yline.set_ydata(y)
        zline.set_ydata(z)

        plt.gca().relim()
        plt.gca().autoscale_view()
        fig.canvas.draw()
        time.sleep(dt)
        fig.canvas.flush_events()

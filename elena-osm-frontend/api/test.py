import pyroutelib3
import os


if __name__ == '__main__':
    start = (42.32683295,-71.61669892134148)
    dest = (42.3185910, -71.6448530)

    r = pyroutelib3.Router("car")

    a, b = r.findNode(start[0],start[1]), r.findNode(dest[0],dest[1])
    s, path = r.doRoute(a, b)
    rnodes = r.get_rnodes()


    lat_min = min(start[0], dest[0])
    lat_max = max(start[0],dest[0])
    long_min = min(start[1],dest[1])
    long_max = max(start[1], dest[1])
    x_markers = []
    y_markers = []

    # for node in path:
    #     x, y = rnodes[node]
    #     x, y = map.to_pixels(x,y)
    #     x_markers.append(x)
    #     y_markers.append(y)
    # ax = map.show_mpl(figsize=(8, 6))
    # x,y = map.to_pixels(start[0], start[1])
    # x1,y1 = map.to_pixels(dest[0], dest[1])

    # ax.plot(x_markers, y_markers,linewidth=5, color='blue')
    # ax.plot(x, y, 'og', ms=10, mew=2)
    # ax.plot(x1, y1, 'or', ms=10, mew=2)
plt.show()
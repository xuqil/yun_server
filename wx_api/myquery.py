from wx_api import models


def query_car(carobj, uid, gid, g_sid):
    """
    查询
    :param carobj: 对应的class
    :param uid: uid
    :param gid: gid
    :param g_sid: g_sid
    :return: 查询结果
    """
    # 使用反射
    if hasattr(models, carobj):
        CarObj = getattr(models, carobj)
    else:
        return None
    car_image = None
    if (gid is None and g_sid is not None) or (gid is None and g_sid is None):
        # gid is not None时该查询没有对某组下的索引进行查询，默认不分组查询
        car_image = CarObj.objects.all().filter(uid_id=uid).order_by('created')
    elif gid is not None and g_sid is None:
        # 只查询组
        car_image = CarObj.objects.all().filter(uid_id=uid).filter(gid=gid).order_by('created')
    elif gid is not None and g_sid is not None:
        # 具体查询
        car_image = CarObj.objects.all().filter(uid_id=uid).filter(gid=gid). \
            filter(g_sid=g_sid).order_by('created')
    return car_image

from app.common.config import cfg

def getSettings():
    filters = cfg.filters.value
    order = cfg.order.value
    return filters, order
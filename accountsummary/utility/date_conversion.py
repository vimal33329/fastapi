from datetime import datetime
def get_days(item):
    if item['start_date'] == 'None' and item['end_date'] == 'None':
        return {
            'total_days': 0,
            'remaining_days': 0,
            'spending_days': 0,
            'rounded_percentage_date': 0,
            "date_color_code": "#c00000"
        }
    else:
        start_date = datetime.strptime(item['start_date'],
                                       '%Y-%m-%d %H:%M:%S') if item and 'start_date' in item else None
        end_date = datetime.strptime(item['end_date'], '%Y-%m-%d %H:%M:%S') if item and 'end_date' in item else None

        now = datetime.now()

        total_delta = end_date - start_date if end_date and start_date else None
        total_days = total_delta.total_seconds() / (24 * 60 * 60) if total_delta else None
        rounded_total_days = round(total_days) if total_days else None

        spending_delta = now - start_date if start_date else None
        spending_days = spending_delta.total_seconds() / (24 * 60 * 60) if spending_delta else None
        rounded_spending_days = round(spending_days) if spending_days else None

        remaining_delta = end_date - now if end_date else None
        remaining_days = remaining_delta.total_seconds() / (24 * 60 * 60) if remaining_delta else None
        rounded_remaining_days = round(remaining_days) if remaining_days else None

        percentage = (spending_days / total_days) * 100 if spending_days and total_days else None
        rounded_percentage = round(percentage, 2) if percentage else None
        if remaining_days<0:
           rounded_percentage =100
        return {
            'total_days': rounded_total_days,
            'remaining_days': rounded_remaining_days,
            'spending_days': rounded_spending_days,
            'rounded_percentage_date': rounded_percentage,
            "date_color_code": "#385723"
        }


def total_calculate(all_object):
    spent_percent = 0
    if all_object["allocated_amount"] is not None and all_object['spent_amount'] is not None:
        spent_percent = (all_object["spent_amount"] / all_object["allocated_amount"]) * 100
        if spent_percent > all_object["rounded_percentage_date"]:
            return {
                "total_spent_percent": round(spent_percent, 2),
                "total_color_code": "#c00000"
            }
        else:
            return {
                "total_spent_percent": round(spent_percent, 2),
                "total_color_code": "#337ab7"
            }
    else:
        return {"total_spent_percent": 0,
                "total_color_code": "#337ab7"
                }

def orange_code(all_object):

  if (all_object["core_spent_percent"] > all_object["rounded_percentage_date"] or all_object["capacity_spent_percent"] > all_object["rounded_percentage_date"] or all_object["capital_spent_percent"] > all_object["rounded_percentage_date"] or all_object['total_spent_percent'] > all_object["rounded_percentage_date"]):
    return {
      "total_color_code": "orange"
    }
  else:
    return {
      "total_color_code": "#337ab7"
    }

def red_code(all_object):
  if (all_object["rounded_percentage_date"] < all_object["total_spent_percent"] ):
    return {
      "total_color_code": "#c00000"
    }

def core_calculate(all_object):
    if all_object["core_allocated_amount"] is not None and all_object['core_spent_amount'] is not None:
        core_spent_percent = (all_object["core_spent_amount"] / all_object["core_allocated_amount"]) * 100
        return {
            "core_spent_percent": round(core_spent_percent, 2),
            "core_color_code": "#337ab7"
        }
    else:
        return {
            "core_spent_percent": 0,
            "core_color_code": "#c00000"
        }


def capacity_calculate(all_object):
    if all_object["capacity_allocated_amount"] is not None and all_object['capacity_spent_amount'] is not None:
        capacity_spent_percent = (all_object["capacity_spent_amount"] / all_object["capacity_allocated_amount"]) * 100
        return {
            "capacity_spent_percent": round(capacity_spent_percent, 2),
            "capacity_color_code": "#337ab7"
        }
    else:
        return {
            "capacity_spent_percent": 0,
            "capacity_color_code": "#c00000"
        }


def capital_calculate(all_object):
    if all_object["capital_allocated_amount"] is not None and all_object['capital_spent_amount'] is not None:
        capital_spent_percent = (all_object["capital_spent_amount"] / all_object["capital_allocated_amount"]) * 100
        return {
            "capital_spent_percent": round(capital_spent_percent, 2),
            "capital_color_code": "#337ab7"
        }
    else:
        return {
            "capital_spent_percent": 0,
            "capital_color_code": "#c00000"
        }


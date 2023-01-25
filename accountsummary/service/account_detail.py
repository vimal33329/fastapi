from db import Database
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from ..utility import date_conversion

db = Database()
def get_acc_details(rsf_id, search_name, starts_with, duration_week, offset, limit):

    if rsf_id is not None and duration_week is not None:
        two_weeks_ago = (datetime.now() - timedelta(weeks=1))
        befTwoWeeksdt = two_weeks_ago.strftime("'%Y-%m-%d %H:%M:%S'")
        # To get total count of users
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                                FROM `resident_accounts`  
                                                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id};""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                AND t.status = 0 AND t.created_by <= {befTwoWeeksdt};""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
                    (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 AND t.created <= {befTwoWeeksdt}) as unapp_count,
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
                    #For getting paid amount
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
                    #Here subtracting deposits - paid to get balance
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance
                    #Conditions and Joins
                    FROM `resident_accounts`
                    WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                    ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} OFFSET {offset};
                    """)
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "homecare"
        return result

    if rsf_id is not None and search_name is None and starts_with is None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                        FROM `resident_accounts`  
                                        WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id};""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                        WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                        AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            #For getting paid amount
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            #Here subtracting deposits - paid to get balance
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance
            #Conditions and Joins
            FROM `resident_accounts`
            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} OFFSET {offset};
            """)
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "homecare"
        return result

    elif rsf_id is not None and search_name is not None and starts_with is None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                        FROM `resident_accounts`  
                                        WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}
                                        AND resident_accounts.lname LIKE '%{search_name}%';""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                                AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            #For getting paid amount
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            #Here subtracting deposits - paid to get balance
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance
            #Conditions and Joins
            FROM `resident_accounts`
            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
            AND resident_accounts.lname LIKE '%{search_name}%'
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} OFFSET {offset};
            """)
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "homecare"
        return result

    elif rsf_id is not None and search_name is None and starts_with is not None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                        FROM `resident_accounts`  
                                        WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}
                                        AND resident_accounts.lname LIKE '{starts_with}%';""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                                AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            #For getting paid amount
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            #Here subtracting deposits - paid to get balance
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance
            #Conditions and Joins
            FROM `resident_accounts`
            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
            AND resident_accounts.lname LIKE '{starts_with}%'
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} OFFSET {offset};
            """)
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "homecare"
        return result

    elif rsf_id is not None and search_name is not None and starts_with is not None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                        FROM `resident_accounts`  
                                        WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}
                                        AND resident_accounts.lname LIKE '%{search_name}%'
                                        AND resident_accounts.lname LIKE '{starts_with}%';""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                                AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            #For getting paid amount
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            #Here subtracting deposits - paid to get balance
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance
            #Conditions and Joins
            FROM `resident_accounts`
            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
            AND resident_accounts.lname LIKE '%{search_name}%'
            AND resident_accounts.lname LIKE '{starts_with}%'
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} OFFSET {offset};
            """)
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "homecare"
        return result

def get_account_ndis(rsf_id, search_name, starts_with, duration_week, offset, limit):
    if rsf_id is not None and duration_week is not None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                                FROM `resident_accounts`  
                                                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id};""")
        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                            FROM `resident_accounts`  
                            LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                            GROUP BY resident_accounts.id
                            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        two_weeks_ago = (datetime.now() - timedelta(weeks=1))
        befTwoWeeksdt = two_weeks_ago.strftime("'%Y-%m-%d %H:%M:%S'")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                AND t.status = 0 AND t.created_by <= {befTwoWeeksdt};""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
                        (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
                        (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
                        (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
                        (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
                        (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
                        (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
                        (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
                        (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
                        (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
                        (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
                        (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
                        (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
                        (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
                        (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
                        (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
                        (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
                        (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
                        FROM `resident_accounts`   
                        WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}  
                        ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "ndis"

        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date": d1,
                "end_date": d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result
    if rsf_id is not None and search_name is None and starts_with is None:

        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                        FROM `resident_accounts`  
                                        WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id};""")
        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                    FROM `resident_accounts`  
                    LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                    WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                    GROUP BY resident_accounts.id
                    ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                                        WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                                        AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
                (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
                FROM `resident_accounts`   
                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}  
                ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "ndis"
        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date":d1,
                "end_date":d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result
    elif rsf_id is not None and search_name is not None and starts_with is None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                                FROM `resident_accounts`  
                                                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}
                                                AND resident_accounts.lname LIKE '%{search_name}%';""")
        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                            FROM `resident_accounts`  
                            LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                            AND resident_accounts.lname LIKE '%{search_name}%'
                            GROUP BY resident_accounts.id
                            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                                                AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
                (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
                FROM `resident_accounts`   
                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                AND resident_accounts.lname LIKE '%{search_name}%' 
                ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "ndis"
        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date": d1,
                "end_date": d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result

    elif rsf_id is not None and search_name is None and starts_with is not None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                                FROM `resident_accounts`  
                                                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}
                                                AND resident_accounts.lname LIKE '{starts_with}%';""")
        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                                    FROM `resident_accounts`  
                                    LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                                    WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                                    AND resident_accounts.lname LIKE '{starts_with}%'
                                    GROUP BY resident_accounts.id
                                    ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                                                AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
                (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
                FROM `resident_accounts`   
                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                AND resident_accounts.lname LIKE '{starts_with}%'
                ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "ndis"
        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date": d1,
                "end_date": d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result

    elif rsf_id is not None and search_name is not None and starts_with is not None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                                                FROM `resident_accounts`  
                                                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id}
                                                AND resident_accounts.lname LIKE '{starts_with}%' 
                                                AND resident_accounts.lname LIKE '%{search_name}%';""")
        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                                            FROM `resident_accounts`  
                                            LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                                            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                                            AND resident_accounts.lname LIKE '{starts_with}%'
                                            AND resident_accounts.lname LIKE '%{search_name}%'
                                            GROUP BY resident_accounts.id
                                            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                                                WHERE resident_accounts.rsf_id = {rsf_id} AND t.invoice_no is not null AND t.spl_id <> 0 
                                                                AND t.status = 0;""")
        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
                (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
                (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
                (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
                (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
                (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
                FROM `resident_accounts`  
                WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
                AND resident_accounts.lname LIKE '{starts_with}%' 
                AND resident_accounts.lname LIKE '%{search_name}%'
                ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "ndis"
        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date": d1,
                "end_date": d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result

def get_account_by_user_id(user_id, search_name, starts_with, duration_week, offset, limit):
    if user_id is not None and duration_week is not None:
        two_weeks_ago = (datetime.now() - timedelta(weeks=1))
        befTwoWeeksdt = two_weeks_ago.strftime("'%Y-%m-%d %H:%M:%S'")
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t 
                                    LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                                    LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                                    WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id}
                                    AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 AND  t.created_by <= {befTwoWeeksdt};;""")
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                        FROM `resident_accounts`  
                        LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                        WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id};""")

        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                        FROM `resident_accounts`  
                        LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
                        LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                        WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
                        GROUP BY resident_accounts.id 
                        ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")

        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
                    (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
                    (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
                    (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
                    (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
                    (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
                    (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
                    (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
                    (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
                    #For Getting Total Capacity Building Amount
                    (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
                    (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
                    (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
                    #For Getting Total Capital Amount
                    (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
                    (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
                    (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
                    FROM `resident_accounts` 
                    LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                    WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
                    ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "ndis"

        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)
        return result
    if user_id is not None and search_name is None and starts_with is None:
        unapproved_count = db.query(query=f"""SELECT count(DISTINCT t.id) as unapp_count FROM transactions t 
                            LEFT JOIN resident_accounts ON t.rsa_id = resident_accounts.id 
                            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id}
                            AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0;""")
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                    FROM `resident_accounts`  
                    LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                    WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id};""")

        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                    FROM `resident_accounts`  
                    LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
                    LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                    WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
                    GROUP BY resident_accounts.id 
                    ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")

        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
            #For Getting Total Capacity Building Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
            #For Getting Total Capital Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
            FROM `resident_accounts` 
            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["unapproved_count"] = unapproved_count
        result["community"] = "ndis"

        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)
        return result

    elif user_id is not None and search_name is not None and starts_with is None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                            FROM `resident_accounts`  
                            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id}
                            AND resident_accounts.lname LIKE '%{search_name}%';""")

        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                            FROM `resident_accounts`  
                            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
                            LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
                            AND resident_accounts.lname LIKE '%{search_name}%'
                            GROUP BY resident_accounts.id 
                            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")

        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
            #For Getting Total Capacity Building Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
            #For Getting Total Capital Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
            FROM `resident_accounts` 
            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
            AND resident_accounts.lname LIKE '%{search_name}%'  
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["community"] = "ndis"

        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date": d1,
                "end_date": d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result
    elif user_id is not None and search_name is None and starts_with is not None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                            FROM `resident_accounts`  
                            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id}
                            AND resident_accounts.lname LIKE '{starts_with}%';""")

        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                                    FROM `resident_accounts`  
                                    LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
                                    LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                                    WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
                                    AND resident_accounts.lname LIKE '{starts_with}%'
                                    GROUP BY resident_accounts.id 
                                    ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")

        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
            #For Getting Total Capacity Building Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
            #For Getting Total Capital Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
            FROM `resident_accounts` 
            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
            AND resident_accounts.lname LIKE '{starts_with}%'  
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["community"] = "ndis"

        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date": d1,
                "end_date": d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result

    elif user_id is not None and search_name is not None and starts_with is not None:
        total_count = db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                            FROM `resident_accounts`  
                            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id}
                            AND resident_accounts.lname LIKE '{starts_with}%'
                            AND resident_accounts.lname LIKE '%{search_name}%';""")

        budget_date = db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
                                    FROM `resident_accounts`  
                                    LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
                                    LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
                                    WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
                                    AND resident_accounts.lname LIKE '{starts_with}%'
                                    AND resident_accounts.lname LIKE '%{search_name}%'
                                    GROUP BY resident_accounts.id 
                                    ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")

        result = db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
            (SELECT count(DISTINCT t.id) as txn_count FROM transactions t WHERE t.rsa_id = resident_accounts.id AND t.invoice_no is not null AND t.spl_id <> 0 AND t.status = 0 ) as unapp_count,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) as deposits,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as paid,
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 1) -
            (SELECT sum(transactions.`txn_amt`) as txn_amt FROM `transactions` WHERE transactions.`rsa_id` = resident_accounts.id AND transactions.type = 0 AND transactions.status = 3) as balance,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id) as remaining_amount,
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCOR') as core_remaining_amount,
            #For Getting Total Capacity Building Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAP') as capacity_remaining_amount,
            #For Getting Total Capital Amount
            (SELECT sum(ndis_support_category_level_details.allocated_amount) as allocated_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_allocated_amount,
            (SELECT sum(ndis_support_category_level_details.spent_amount) as spent_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_spent_amount,
            (SELECT sum(ndis_support_category_level_details.remaining_amount) as remaining_amount FROM `ndis_support_category_level_details` WHERE ndis_support_category_level_details.`rsa_id` = resident_accounts.id AND ndis_support_category_level_details.support_type = 'ZCAT') as capital_remaining_amount
            FROM `resident_accounts` 
            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
            AND resident_accounts.lname LIKE '{starts_with}%'
            AND resident_accounts.lname LIKE '%{search_name}%' 
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
        result["total_count"] = total_count['result'][0]['total_count']
        result["community"] = "ndis"

        for obj in budget_date['result']:
            for first_obj in result['result']:
                if first_obj['id'] == obj['id']:
                    first_obj.update(obj)

        for dates in result['result']:
            d1 = str(dates['start_date'])
            d2 = str(dates['end_date'])
            item = {
                "start_date": d1,
                "end_date": d2
            }
            res = date_conversion.get_days(item)
            dates.update(res)

        for objcolorcode in result['result']:
            res1 = date_conversion.total_calculate(objcolorcode)
            res2 = date_conversion.core_calculate(objcolorcode)
            res3 = date_conversion.capacity_calculate(objcolorcode)
            res4 = date_conversion.capital_calculate(objcolorcode)
            objcolorcode.update(res1)
            objcolorcode.update(res2)
            objcolorcode.update(res3)
            objcolorcode.update(res4)

        for objorangeccode in result['result']:
            orange_res = date_conversion.total_calculate(objorangeccode)
            objorangeccode.update(orange_res)
            oran = date_conversion.orange_code(objorangeccode)
            objorangeccode.update(oran)

        return result

def get_ndis(rsf_id):
    if rsf_id is not None:
        get_ndis_id = db.query(query=f"""SELECT rf.id from residential_facilities as rf 
            INNER JOIN templates temp ON temp.id = rf.temp_id WHERE temp.invoice_ndis = 1 and rf.id = {rsf_id};""")
        return (get_ndis_id)

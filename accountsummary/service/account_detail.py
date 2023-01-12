from db import Database
from fastapi import HTTPException, status
db = Database()
def get_acc_details(rsf_id, search_by_lname, starts_with, offset, limit):
    if rsf_id is not None and search_by_lname is None and starts_with is None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
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
    elif rsf_id is not None and search_by_lname is not None and starts_with is None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
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
            AND resident_accounts.lname LIKE '%{search_by_lname}%'
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} OFFSET {offset};
            """)
    elif rsf_id is not None and search_by_lname is None and starts_with is not None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
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
    elif rsf_id is not None and search_by_lname is not None and starts_with is not None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id,
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
            AND resident_accounts.lname LIKE '%{search_by_lname}%'
            AND resident_accounts.lname LIKE '{starts_with}%'
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} OFFSET {offset};
            """)

def get_account_ndis(rsf_id, search_by_lname, starts_with, offset, limit):
    if rsf_id is not None and search_by_lname is None and starts_with is None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
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
    elif rsf_id is not None and search_by_lname is not None and starts_with is None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
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
                AND resident_accounts.lname LIKE '%{search_by_lname}%' 
                ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
    elif rsf_id is not None and search_by_lname is None and starts_with is not None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
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
    elif rsf_id is not None and search_by_lname is not None and starts_with is not None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, resident_accounts.rsf_id, 
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
                AND resident_accounts.lname LIKE '%{search_by_lname}%'
                ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")

def get_account_by_user_id(user_id, search_by_lname, starts_with, offset, limit):
    if user_id is not None and search_by_lname is None and starts_with is None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
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
    elif user_id is not None and search_by_lname is not None and starts_with is None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
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
            AND resident_accounts.lname LIKE '%{search_by_lname}%'  
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")
    elif user_id is not None and search_by_lname is None and starts_with is not None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
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
    elif user_id is not None and search_by_lname is not None and starts_with is not None:
        return db.query(query=f"""SELECT resident_accounts.id, resident_accounts.lname, resident_accounts.fname, 
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
            AND resident_accounts.lname LIKE '%{search_by_lname}%' 
            ORDER BY `resident_accounts`.`lname` ASC LIMIT {limit} offset {offset};""")

def get_budget_date(rsf_id, user_id):
    if rsf_id is not None:
        return db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
            FROM `resident_accounts`  
            LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
            WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id} 
            GROUP BY resident_accounts.id
            ORDER BY `resident_accounts`.`lname` ASC LIMIT 20;""")
    if user_id is not None:
        return db.query(query=f"""SELECT resident_accounts.id, ndis_support_category_level_details.start_date, ndis_support_category_level_details.end_date
            FROM `resident_accounts`  
            LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id 
            LEFT JOIN ndis_support_category_level_details ON ndis_support_category_level_details.rsa_id = resident_accounts.id 
            WHERE resident_accounts.archived = 0 AND account_viewers.user_id = {user_id} 
            GROUP BY resident_accounts.id 
            ORDER BY `resident_accounts`.`lname` ASC LIMIT 20;""")

def get_ndis(rsf_id):
    if rsf_id is not None:
        get_ndis_id = db.query(query=f"""SELECT rf.id from residential_facilities as rf 
            INNER JOIN templates temp ON temp.id = rf.temp_id WHERE temp.invoice_ndis = 1 and rf.id = {rsf_id};""")
        return (get_ndis_id)

def get_count_for_pagination(rsf_id, user_id):
    if rsf_id is not None:
        return  db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                    FROM `resident_accounts`  
                    WHERE resident_accounts.archived = 0 AND resident_accounts.rsf_id = {rsf_id};""")
    if user_id is not None:
        return db.query(query=f"""SELECT count(resident_accounts.id) as total_count
                    FROM `resident_accounts`  
                    LEFT JOIN account_viewers ON account_viewers.rsa_id = resident_accounts.id
                    WHERE resident_accounts.archived = 0 AND AND account_viewers.user_id = {user_id};""")

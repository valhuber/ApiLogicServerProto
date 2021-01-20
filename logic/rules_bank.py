from logic_bank.logic_bank import Rule
from database import models


def declare_logic():
    pass
    # use code completion to declare rules here

    print("\n\ndeclare_logic")

    """ example from default database
    
    Rule.constraint(validate=models.Customer,
                    as_condition=lambda row: row.Balance <= row.CreditLimit,
                    error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
    
    """

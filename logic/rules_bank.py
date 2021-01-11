from logic_bank.logic_bank import Rule
from database.models import StoreModel, ItemModel


def declare_logic():

    Rule.constraint(validate=StoreModel,
                    as_condition=lambda row: 'X' not in row.name,
                    error_msg="Store Names({row.name}) should not contain X")
    Rule.count(StoreModel.item_count, as_count_of=ItemModel)
    Rule.parent_check(validate=ItemModel, error_msg="no parent", enable=True)

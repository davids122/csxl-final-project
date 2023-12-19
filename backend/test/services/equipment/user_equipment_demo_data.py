"""Mock data for equipment demo.

"""

from enum import Enum
import pytest
from sqlalchemy.orm import Session
from backend.entities.equipment_entity import EquipmentEntity
from backend.entities.permission_entity import PermissionEntity
from backend.models.equipment import Equipment
from backend.models.permission import Permission
from backend.test.services.reset_table_id_seq import reset_table_id_seq
from backend.test.services.role_data import ambassador_role


__authors__ = ["Ayden Franklin"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


# enum storing png images for each equipment type
class DeviceType(Enum):
    META_QUEST_3 = "https://s7d1.scene7.com/is/image/dmqualcommprod/meta-quest-3-1?$QC_Responsive$&fmt=png-alpha"

    ARDUINO_UNO = (
        "https://www.circuitbasics.com/wp-content/uploads/2020/05/Arduino-Uno.png"
    )

    IPAD_AIR = "https://www.stmgoods.com/wp-content/uploads/STM22-Studio-MultiFit-iPad-Air-5th-gen-Pro-3rd-gen-Black-Quarter-Front.png"

    ANDROID = "https://image-us.samsung.com/SamsungUS/home/mobile/phones/pdp/galaxy-s21-fe-5g/gallery/SM-G990U-graphite-1.png"


# Create all the equipment for the demo

quest3_1 = Equipment(
    equipment_id=1,
    model="Meta Quest 3",
    equipment_image=DeviceType.META_QUEST_3.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

quest3_2 = Equipment(
    equipment_id=2,
    model="Meta Quest 3",
    equipment_image=DeviceType.META_QUEST_3.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

quest3_3 = Equipment(
    equipment_id=3,
    model="Meta Quest 3",
    equipment_image=DeviceType.META_QUEST_3.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

arduino_1 = Equipment(
    equipment_id=4,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

arduino_2 = Equipment(
    equipment_id=5,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

arduino_3 = Equipment(
    equipment_id=6,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

ipad_1 = Equipment(
    equipment_id=7,
    model="Ipad",
    equipment_image=DeviceType.IPAD_AIR.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

ipad_2 = Equipment(
    equipment_id=8,
    model="Ipad",
    equipment_image=DeviceType.IPAD_AIR.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

ipad_3 = Equipment(
    equipment_id=9,
    model="Ipad",
    equipment_image=DeviceType.IPAD_AIR.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

android_1 = Equipment(
    equipment_id=10,
    model="Android",
    equipment_image=DeviceType.ANDROID.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

android_2 = Equipment(
    equipment_id=11,
    model="Android",
    equipment_image=DeviceType.ANDROID.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

# create permissions for the demo

ambassador_permission_crud_checkout = Permission(
    id=4, action="equipment.crud.checkout", resource="equipment"
)

ambassador_permission_view_checkout = Permission(
    id=5, action="equipment.view.checkout", resource="equipment"
)

equipment = [
    quest3_1,
    quest3_2,
    quest3_3,
    arduino_1,
    arduino_2,
    arduino_3,
    ipad_1,
    ipad_2,
    ipad_3,
    android_1,
    android_2,
]

permissions = [ambassador_permission_crud_checkout, ambassador_permission_view_checkout]


def insert_fake_data(session: Session):
    global equipment

    # insert equipment entities into the demo
    equipment_entities = []
    for item in equipment:
        entity = EquipmentEntity.from_model(item)
        session.add(entity)
        equipment_entities.append(entity)

    # insert permission entities into the demo
    permission_entities = []
    for i in range(0, len(permissions)):
        entity = PermissionEntity(
            id=permissions[i].id,
            role_id=ambassador_role.id,
            action=permissions[i].action,
            resource=permissions[i].resource,
        )
        session.add(entity)
        permission_entities.append(entity)

    # reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, EquipmentEntity, EquipmentEntity.id, len(equipment) + 1)
    reset_table_id_seq(
        session, PermissionEntity, PermissionEntity.id, len(permissions) + 1
    )

    # commit the demo data
    session.commit()

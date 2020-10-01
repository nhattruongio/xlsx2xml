import re
# import unidecode  #THƯ VIỆN DECODE UNICODE - CHUYỂN TIẾNG VIỆT SANG KHÔNG DẤU
# ĐỌC FILE
import json
with open("json/dvhcvn.json") as json_file:
    dicts = json.load(json_file)

# CHUYỂN TIẾNG VIỆT SANG KHÔNG DẤU
def unidecode_vn(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
    # EX : unidecode_vn(<string>)

# KHUÔN MẪU
pattern = """
    <record id="{record_id}" model="{model_name}">
        <field name="code">{record_code}</field>
        <field name="name">{record_name}</field>
        <field name="type">{record_type}</field>
        <field name="en_name">{record_name_en}</field>
        <field name="district_id" ref="{record_district_id}"/>
    </record>"""

state = 'base.state_vn_VN-'
model_name = 'res.district.ward'

results = ['''<?xml version='1.0' encoding='utf-8'?>
<odoo>''',
]

data = dicts['data']
vals = ''
valss = ''
en_vals = []


for city in data:
    city_name = city['name']
    for district in city['level2s']:
        strs = unidecode_vn(district['name'])
        # # strs = unidecode.unidecode(district['name'])
        # vals = strs.split(" ")
        # if vals[0] == 'Huyen' or vals[0] == 'Quan':
        #     en_vals = vals[1:] + ['District']
        # if vals[0] == 'Thanh' or vals[1] == 'Pho':
        #     city = vals[0] +' '+ vals [1]
        #     en_vals = vals[2:] + ['City']
        # if vals[0] == 'Thi' or vals[1] == 'Xa':
        #     town = vals[0] +' '+ vals [1]
        #     en_vals = ['Town'] + vals[2:]
        # value = ' '.join(map(str, en_vals))
        # recode_define = pattern.format(
        #     record_id = 'res_district_' + district['level2_id'] or '',
        #     model_name = model_name or '',
        #     record_name = district['name'] or '',
        #     record_code = district['level2_id'] or '',
        #     record_type =district['type'],
        #     record_name_en = value or '',
        #     record_state_id = city_name or ''
        # )
        for ward in district['level3s']:
            strs2 = unidecode_vn(ward['name'])
            vals2 = strs2.split(" ")

            if vals2[0] == 'Phuong':
                en_vals = vals2[1:] + ['Ward']
            if vals2[0] == 'Xa':
                en_vals = vals2[1:] + ['Commune']
            if vals2[0] == 'Thi' or vals2[1] == 'tran':
                town = vals2[0] +' '+ vals2[1]
                en_vals = vals2[2:] + ['Town']
           
            value = ' '.join(map(str, en_vals))
            
            if ward['type'] == 'Phường':
                ward['type'] = 'ward'
            if  ward['type'] == 'Xã':
                ward['type'] = 'commune'
            if ward['type'] == 'Thị trấn':
                ward['type'] = 'town'

            recode_define = pattern.format(
                record_id = 'res_district_ward_' + ward['level3_id'] or '',
                model_name = model_name or '',
                record_name = ward['name'] or '',
                record_code = ward['level3_id'] or '',
                record_type =ward['type'],
                record_name_en = value or '',
                record_district_id = 'res_district_' + district['level2_id'] or ''
            )
            type = ward['type']
            results.append(recode_define)

results.append(
'''
</odoo>
'''
)

vals = '\n'.join(results)

# GHI FILE
with open("master_data/res_country_vn/res.xml", "w") as file:
    file.write(str(vals))
print('''
###################TRUONGPN####################
#                                             #
# ..................SUCCES....................#
#                                             #
###############################################
''')
from flask import Flask, jsonify, render_template
import random
import io
from flask import Response
from xlsxwriter import Workbook

app = Flask(__name__, template_folder='templates')  # 指定模板文件夹路径

# 定义奖品列表
prizes = {
    "1元卷": 10,
    "5元卷": 5,
    "10元卷": 3,
    "1元提现": 2,
    "2元提现": 1,
    "5元提现": 1,
    "100积分": 10,
    "1包抽纸": 5,
    "谢谢惠顾": 10
}

# 定义抽奖函数
def drawLottery():
    # 根据奖品数量生成权重
    weights = [prizes[prize] for prize in prizes]
    # 使用 random.choices 选择奖品
    prize = random.choices(list(prizes.keys()), weights=weights)[0]
    # 计算奖品索引
    prizeIndex = list(prizes.keys()).index(prize)
    # 返回奖品和索引
    return prize, prizeIndex

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lottery', methods=['GET'])
def lottery():
    # 调用抽奖函数获取结果
    prize, prizeIndex = drawLottery()
    # 获取所有奖品列表
    prizes_list = list(prizes.keys())
    # 返回 JSON 格式的结果
    return jsonify({'prize': prize, 'prizeIndex': prizeIndex, 'prizes': prizes_list})

@app.route('/export', methods=['GET'])
def export():
    # 获取中奖结果列表
    results = [{'user': '用户1', 'prize': '1元卷'}, {'user': '用户2', 'prize': '5元卷'}]
    # 创建 Excel 文件
    output = io.BytesIO()
    workbook = Workbook(output)
    worksheet = workbook.add_worksheet()
    # 写入表头
    worksheet.write('A1', '用户')
    worksheet.write('B1', '奖品')
    # 写入中奖结果
    for index, result in enumerate(results, start=1):
        worksheet.write(f'A{index+1}', result['user'])
        worksheet.write(f'B{index+1}', result['prize'])
    # 关闭文件
    workbook.close()
    output.seek(0)
    # 返回 Excel 文件
    return Response(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-disposition": "attachment; filename=lottery_results.xlsx"})

if __name__ == '__main__':
    app.run(debug=True)

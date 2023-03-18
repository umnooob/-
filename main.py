from PIL import Image, ImageFont

from handright import Template, handwrite
from multiprocessing import Pool
from date import count_businessday
from tqdm import tqdm

start_day = '2022-11-06'
end_day = '2022-11-11'
week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

if __name__ == "__main__":
    bg = Image.open("./bg.png", 'r').convert(mode="L")
    width, height = bg.size
    bg = bg.resize((width * 2, height * 2), resample=Image.LANCZOS)

    template = Template(
        background=bg,
        font=ImageFont.truetype("./云烟体.ttf", size=120), #可以传入任意字体
        line_spacing=158,
        fill=0,  # 字体“颜色”
        left_margin=225,
        top_margin=40,
        right_margin=225,
        bottom_margin=150,
        word_spacing=2.1,
        line_spacing_sigma=1,  # 行间距随机扰动
        font_size_sigma=8,  # 字体大小随机扰动
        word_spacing_sigma=0.4,  # 字间距随机扰动
        start_chars="“（[<",  # 特定字符提前换行，防止出现在行尾
        end_chars="，。",  # 防止特定字符因排版算法的自动换行而出现在行首
        perturb_x_sigma=4,  # 笔画横向偏移随机扰动
        perturb_y_sigma=4,  # 笔画纵向偏移随机扰动
        perturb_theta_sigma=0.05,  # 笔画旋转偏移随机扰动
    )
    weeks = count_businessday(start_day=start_day, end_day=end_day)
    for i, week in enumerate(tqdm(weeks)):
        with open(f'./report/{i+1}.txt', encoding='utf-8') as f:
            file = f.read()
        spilt_file = file.split('---')
        assert len(spilt_file) == len(week)
        new_text = []
        for id, split_item in enumerate(spilt_file):
            if id == 0:
                new_text.append(week[id].strftime('%Y年%m月%d日  ') + week_list[week[id].weekday()] + '\n' + split_item)
            else:
                new_text.append(week[id].strftime('%Y年%m月%d日  ') + week_list[week[id].weekday()] + split_item)
        text = '\n'.join(new_text)

        with Pool() as p:
            images = handwrite(text, template, mapper=p.map)
            for idx, im in enumerate(tqdm(images)):
                assert isinstance(im, Image.Image)
                im.save(f"./export/{i+1}_{idx}.pdf", "PDF", resolution=300.0)
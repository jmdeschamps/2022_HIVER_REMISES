from PIL import Image, ImageDraw, ImageTk


def VaisseauGuerre(couleur, angle):
	img_size_px = 128
	line_color = (255, 100, 100)
	line_vaisseau = couleur
	line_blue = (0, 0, 255)
	grosseur = 8

	img = Image.new("RGBA", size=(img_size_px, img_size_px))

	draw = ImageDraw.Draw(img)

	line_1G = ((8, 64), (8, 80))
	line_2G = ((8, 80), (8, 128))

	line_3G = ((16, 96), (16, 120))

	line_4G = ((24, 88), (24, 112))

	line_5G = ((32, 48), (32, 64))
	line_6G = ((32, 64), (32, 72))
	line_7G = ((32, 72), (32, 80))
	line_8G = ((32, 80), (32, 104))

	line_9G = ((40, 64), (40, 72))
	line_10G = ((40, 72), (40, 104))
	line_11G = ((40, 104), (40, 120))

	line_12G = ((48, 56), (48, 96))
	line_13G = ((48, 96), (48, 120))

	line_14G = ((56, 24), (56, 72))
	line_15G = ((56, 72), (56, 88))
	line_16G = ((56, 88), (56, 112))

	line_c1 = ((64, 0), (64, 64))
	line_c2 = ((64, 64), (64, 80))
	line_c3 = ((64, 80), (64, 128))

	line_16D = ((72, 88), (72, 112))
	line_15D = ((72, 72), (72, 88))
	line_14D = ((72, 24), (72, 72))

	line_13D = ((80, 96), (80, 120))
	line_12D = ((80, 56), (80, 96))

	line_11D = ((88, 104), (88, 120))
	line_10D = ((88, 72), (88, 104))
	line_9D = ((88, 64), (88, 72))

	line_8D = ((96, 80), (96, 104))
	line_7D = ((96, 72), (96, 80))
	line_6D = ((96, 64), (96, 72))
	line_5D = ((96, 48), (96, 64))

	line_4D = ((104, 88), (104, 112))

	line_3D = ((112, 96), (112, 120))

	line_2D = ((120, 80), (120, 128))
	line_1D = ((120, 64), (120, 80))

	draw.line(line_1G, fill=line_color, width=grosseur)
	draw.line(line_2G, fill=line_vaisseau, width=grosseur)
	draw.line(line_3G, fill=line_vaisseau, width=grosseur)
	draw.line(line_4G, fill=line_vaisseau, width=grosseur)
	draw.line(line_5G, fill=line_color, width=grosseur)
	draw.line(line_6G, fill=line_vaisseau, width=grosseur)
	draw.line(line_7G, fill=line_blue, width=grosseur)
	draw.line(line_8G, fill=line_vaisseau, width=grosseur)
	draw.line(line_9G, fill=line_blue, width=grosseur)
	draw.line(line_10G, fill=line_vaisseau, width=grosseur)
	draw.line(line_11G, fill=line_color, width=grosseur)
	draw.line(line_12G, fill=line_vaisseau, width=grosseur)
	draw.line(line_13G, fill=line_color, width=grosseur)
	draw.line(line_14G, fill=line_vaisseau, width=grosseur)
	draw.line(line_15G, fill=line_color, width=grosseur)
	draw.line(line_16G, fill=line_vaisseau, width=grosseur)
	draw.line(line_c1, fill=line_vaisseau, width=grosseur)
	draw.line(line_c2, fill=line_color, width=grosseur)
	draw.line(line_c3, fill=line_vaisseau, width=grosseur)
	draw.line(line_1D, fill=line_color, width=grosseur)
	draw.line(line_2D, fill=line_vaisseau, width=grosseur)
	draw.line(line_3D, fill=line_vaisseau, width=grosseur)
	draw.line(line_4D, fill=line_vaisseau, width=grosseur)
	draw.line(line_5D, fill=line_color, width=grosseur)
	draw.line(line_6D, fill=line_vaisseau, width=grosseur)
	draw.line(line_7D, fill=line_blue, width=grosseur)
	draw.line(line_8D, fill=line_vaisseau, width=grosseur)
	draw.line(line_9D, fill=line_blue, width=grosseur)
	draw.line(line_10D, fill=line_vaisseau, width=grosseur)
	draw.line(line_11D, fill=line_color, width=grosseur)
	draw.line(line_12D, fill=line_vaisseau, width=grosseur)
	draw.line(line_13D, fill=line_color, width=grosseur)
	draw.line(line_14D, fill=line_vaisseau, width=grosseur)
	draw.line(line_15D, fill=line_color, width=grosseur)
	draw.line(line_16D, fill=line_vaisseau, width=grosseur)

	newsize = (25, 25)

	im11 = img.rotate(angle)
	out1 = im11.resize(newsize)
	python_image = ImageTk.PhotoImage(out1)
	return python_image


def VaisseauScout(couleur, angle):
	img_size_px = 128
	line_color = (0, 0, 0)
	line_vaisseau = couleur
	line_blue = (0, 0, 255)
	grosseur = 4

	img_vaisseauscout = Image.new("RGBA", size=(img_size_px, img_size_px))

	draw = ImageDraw.Draw(img_vaisseauscout)

	line_1G = ((4, 104), (4, 108))

	line_2G = ((8, 100), (8, 108))

	line_3G = ((12, 96), (12, 100))
	line_4G = ((12, 100), (12, 104))
	line_5G = ((12, 104), (12, 108))

	line_6G = ((16, 92), (16, 96))
	line_7G = ((16, 96), (16, 100))
	line_8G = ((16, 100), (16, 104))

	line_9G = ((20, 88), (20, 92))
	line_10G = ((20, 92), (20, 100))
	line_11G = ((20, 100), (20, 104))

	line_12G = ((24, 80), (24, 92))
	line_13G = ((24, 92), (24, 96))
	line_14G = ((24, 96), (24, 100))

	line_15G = ((28, 64), (28, 100))

	line_16G = ((32, 48), (32, 64))
	line_17G = ((32, 64), (32, 84))
	line_18G = ((32, 84), (32, 96))

	line_19G = ((36, 32), (36, 48))
	line_20G = ((36, 48), (36, 64))
	line_21G = ((36, 64), (36, 84))
	line_22G = ((36, 84), (36, 88))
	line_23G = ((36, 88), (36, 96))

	line_24G = ((40, 16), (40, 40))
	line_25G = ((40, 40), (40, 48))
	line_26G = ((40, 48), (40, 84))
	line_27G = ((40, 84), (40, 88))
	line_28G = ((40, 88), (40, 96))

	line_29G = ((44, 0), (44, 20))
	line_30G = ((44, 20), (44, 32))
	line_31G = ((44, 32), (44, 36))
	line_32G = ((44, 36), (44, 40))
	line_33G = ((44, 40), (44, 84))
	line_34G = ((44, 84), (44, 88))
	line_35G = ((44, 88), (44, 96))

	line_35D = ((48, 88), (48, 96))
	line_34D = ((48, 84), (48, 88))
	line_33D = ((48, 40), (48, 84))
	line_32D = ((48, 36), (48, 40))
	line_31D = ((48, 32), (48, 36))
	line_30D = ((48, 20), (48, 32))
	line_29D = ((48, 0), (48, 20))

	line_28D = ((52, 88), (52, 96))
	line_27D = ((52, 84), (52, 88))
	line_26D = ((52, 48), (52, 84))
	line_25D = ((52, 40), (52, 48))
	line_24D = ((52, 16), (52, 40))

	line_23D = ((56, 88), (56, 96))
	line_22D = ((56, 84), (56, 88))
	line_21D = ((56, 64), (56, 84))
	line_20D = ((56, 48), (56, 64))
	line_19D = ((56, 32), (56, 48))

	line_18D = ((60, 84), (60, 96))
	line_17D = ((60, 64), (60, 84))
	line_16D = ((60, 48), (60, 64))

	line_15D = ((64, 64), (64, 100))

	line_14D = ((68, 96), (68, 100))
	line_13D = ((68, 92), (68, 96))
	line_12D = ((68, 80), (68, 92))

	line_11D = ((72, 100), (72, 104))
	line_10D = ((72, 92), (72, 100))
	line_9D = ((72, 88), (72, 92))

	line_8D = ((76, 100), (76, 104))
	line_7D = ((76, 96), (76, 100))
	line_6D = ((76, 92), (76, 96))

	line_5D = ((80, 104), (80, 108))
	line_4D = ((80, 100), (80, 104))
	line_3D = ((80, 96), (80, 100))

	line_2D = ((84, 100), (84, 108))

	line_1D = ((88, 104), (88, 108))

	draw.line(line_1G, fill=line_vaisseau, width=grosseur)
	draw.line(line_2G, fill=line_vaisseau, width=grosseur)
	draw.line(line_3G, fill=line_vaisseau, width=grosseur)
	draw.line(line_4G, fill=line_color, width=grosseur)
	draw.line(line_5G, fill=line_vaisseau, width=grosseur)
	draw.line(line_6G, fill=line_vaisseau, width=grosseur)
	draw.line(line_7G, fill=line_color, width=grosseur)
	draw.line(line_8G, fill=line_vaisseau, width=grosseur)
	draw.line(line_9G, fill=line_vaisseau, width=grosseur)
	draw.line(line_10G, fill=line_color, width=grosseur)
	draw.line(line_11G, fill=line_vaisseau, width=grosseur)
	draw.line(line_12G, fill=line_vaisseau, width=grosseur)
	draw.line(line_13G, fill=line_color, width=grosseur)
	draw.line(line_14G, fill=line_vaisseau, width=grosseur)
	draw.line(line_15G, fill=line_vaisseau, width=grosseur)
	draw.line(line_16G, fill=line_vaisseau, width=grosseur)
	draw.line(line_17G, fill=line_color, width=grosseur)
	draw.line(line_18G, fill=line_vaisseau, width=grosseur)
	draw.line(line_19G, fill=line_vaisseau, width=grosseur)
	draw.line(line_20G, fill=line_color, width=grosseur)
	draw.line(line_21G, fill=line_blue, width=grosseur)
	draw.line(line_22G, fill=line_color, width=grosseur)
	draw.line(line_23G, fill=line_vaisseau, width=grosseur)
	draw.line(line_24G, fill=line_vaisseau, width=grosseur)
	draw.line(line_25G, fill=line_color, width=grosseur)
	draw.line(line_26G, fill=line_blue, width=grosseur)
	draw.line(line_27G, fill=line_color, width=grosseur)
	draw.line(line_28G, fill=line_vaisseau, width=grosseur)
	draw.line(line_29G, fill=line_vaisseau, width=grosseur)
	draw.line(line_30G, fill=line_color, width=grosseur)
	draw.line(line_31G, fill=line_vaisseau, width=grosseur)
	draw.line(line_32G, fill=line_color, width=grosseur)
	draw.line(line_33G, fill=line_blue, width=grosseur)
	draw.line(line_34G, fill=line_color, width=grosseur)
	draw.line(line_35G, fill=line_vaisseau, width=grosseur)
	draw.line(line_1D, fill=line_vaisseau, width=grosseur)
	draw.line(line_2D, fill=line_vaisseau, width=grosseur)
	draw.line(line_3D, fill=line_vaisseau, width=grosseur)
	draw.line(line_4D, fill=line_color, width=grosseur)
	draw.line(line_5D, fill=line_vaisseau, width=grosseur)
	draw.line(line_6D, fill=line_vaisseau, width=grosseur)
	draw.line(line_7D, fill=line_color, width=grosseur)
	draw.line(line_8D, fill=line_vaisseau, width=grosseur)
	draw.line(line_9D, fill=line_vaisseau, width=grosseur)
	draw.line(line_10D, fill=line_color, width=grosseur)
	draw.line(line_11D, fill=line_vaisseau, width=grosseur)
	draw.line(line_12D, fill=line_vaisseau, width=grosseur)
	draw.line(line_13D, fill=line_color, width=grosseur)
	draw.line(line_14D, fill=line_vaisseau, width=grosseur)
	draw.line(line_15D, fill=line_vaisseau, width=grosseur)
	draw.line(line_16D, fill=line_vaisseau, width=grosseur)
	draw.line(line_17D, fill=line_color, width=grosseur)
	draw.line(line_18D, fill=line_vaisseau, width=grosseur)
	draw.line(line_19D, fill=line_vaisseau, width=grosseur)
	draw.line(line_20D, fill=line_color, width=grosseur)
	draw.line(line_21D, fill=line_blue, width=grosseur)
	draw.line(line_22D, fill=line_color, width=grosseur)
	draw.line(line_23D, fill=line_vaisseau, width=grosseur)
	draw.line(line_24D, fill=line_vaisseau, width=grosseur)
	draw.line(line_25D, fill=line_color, width=grosseur)
	draw.line(line_26D, fill=line_blue, width=grosseur)
	draw.line(line_27D, fill=line_color, width=grosseur)
	draw.line(line_28D, fill=line_vaisseau, width=grosseur)
	draw.line(line_29D, fill=line_vaisseau, width=grosseur)
	draw.line(line_30D, fill=line_color, width=grosseur)
	draw.line(line_31D, fill=line_vaisseau, width=grosseur)
	draw.line(line_32D, fill=line_color, width=grosseur)
	draw.line(line_33D, fill=line_blue, width=grosseur)
	draw.line(line_34D, fill=line_color, width=grosseur)
	draw.line(line_35D, fill=line_vaisseau, width=grosseur)

	newsize = (25, 25)

	im11 = img_vaisseauscout.rotate(angle)
	out111 = im11.resize(newsize)

	python_image = ImageTk.PhotoImage(out111)
	return python_image

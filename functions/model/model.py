import torch
import torch.nn as nn


class DECBR3d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True, norm="bnorm", relu=0.0):
        super().__init__()

        layers = []
        layers += [nn.ConvTranspose3d(in_channels=in_channels, out_channels=out_channels,
                                      kernel_size=kernel_size, stride=stride, padding=padding,
                                      bias=bias)]

        if not norm is None:
            if norm == "bnorm":
                layers += [nn.BatchNorm3d(num_features=out_channels)]
            elif norm == "inorm":
                layers += [nn.InstanceNorm3d(num_features=out_channels)]

        if not relu is None and relu >= 0.0:
            layers += [nn.ReLU() if relu == 0 else nn.LeakyReLU(relu)]

        self.cbr = nn.Sequential(*layers)

    def forward(self, x):
        return self.cbr(x)


class CBR3d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True, norm="bnorm", relu=0.0):
        super().__init__()

        layers = []
        layers += [nn.Conv3d(in_channels=in_channels, out_channels=out_channels,
                             kernel_size=kernel_size, stride=stride, padding=padding,
                             bias=bias)]

        if not norm is None:
            if norm == "bnorm":
                layers += [nn.BatchNorm3d(num_features=out_channels)]
            elif norm == "inorm":
                layers += [nn.InstanceNorm3d(num_features=out_channels)]

        if not relu is None and relu >= 0.0:
            layers += [nn.ReLU() if relu == 0 else nn.LeakyReLU(relu)]

        self.cbr = nn.Sequential(*layers)

    def forward(self, x):
        return self.cbr(x)


class Pix2Pix_3D(nn.Module):
    def __init__(self, in_channels, out_channels, nker=64, norm="bnorm"):
        super(Pix2Pix_3D, self).__init__()

        self.enc1 = CBR3d(in_channels, 1 * nker, kernel_size=4, padding=1,
                          norm=None, relu=0.2, stride=2)

        self.enc2 = CBR3d(1 * nker, 2 * nker, kernel_size=4, padding=1,
                          norm=norm, relu=0.2, stride=2)

        self.enc3 = CBR3d(2 * nker, 4 * nker, kernel_size=4, padding=1,
                          norm=norm, relu=0.2, stride=2)

        self.enc4 = CBR3d(4 * nker, 8 * nker, kernel_size=4, padding=1,
                          norm=norm, relu=0.2, stride=2)

        self.enc5 = CBR3d(8 * nker, 8 * nker, kernel_size=4, padding=1,
                          norm=norm, relu=0.2, stride=2)

        self.enc6 = CBR3d(8 * nker, 8 * nker, kernel_size=4, padding=1,
                          norm=norm, relu=0.2, stride=2)

        self.enc7 = CBR3d(8 * nker, 8 * nker, kernel_size=4, padding=1,
                          norm=norm, relu=0.2, stride=2)

        self.enc8 = CBR3d(8 * nker, 8 * nker, kernel_size=4, padding=1,
                          norm=norm, relu=0.2, stride=2)


        self.dec1 = DECBR3d(8 * nker, 8 * nker, kernel_size=4, padding=1,
                            norm=norm, relu=0.0, stride=2)
        self.drop1 = nn.Dropout3d(0.5)

        self.dec2 = DECBR3d(2 * 8 * nker, 8 * nker, kernel_size=4, padding=1,
                            norm=norm, relu=0.0, stride=2)
        self.drop2 = nn.Dropout3d(0.5)

        self.dec3 = DECBR3d(2 * 8 * nker, 8 * nker, kernel_size=4, padding=1,
                            norm=norm, relu=0.0, stride=2)
        self.drop3 = nn.Dropout3d(0.5)

        self.dec4 = DECBR3d(2 * 8 * nker, 8 * nker, kernel_size=4, padding=1,
                            norm=norm, relu=0.0, stride=2)

        self.dec5 = DECBR3d(2 * 8 * nker, 4 * nker, kernel_size=4, padding=1,
                            norm=norm, relu=0.0, stride=2)

        self.dec6 = DECBR3d(2 * 4 * nker, 2 * nker, kernel_size=4, padding=1,
                            norm=norm, relu=0.0, stride=2)

        self.dec7 = DECBR3d(2 * 2 * nker, 1 * nker, kernel_size=4, padding=1,
                            norm=norm, relu=0.0, stride=2)

        self.dec8 = DECBR3d(2 * 1 * nker, out_channels, kernel_size=4, padding=1,
                            norm=None, relu=None, stride=2)

    def forward(self, x):
        enc1 = self.enc1(x)
        enc2 = self.enc2(enc1)
        enc3 = self.enc3(enc2)
        enc4 = self.enc4(enc3)
        enc5 = self.enc5(enc4)
        enc6 = self.enc6(enc5)
        enc7 = self.enc7(enc6)
        enc8 = self.enc8(enc7)

        dec1 = self.dec1(enc8)
        drop1 = self.drop1(dec1)

        cat2 = torch.cat((drop1, enc7), dim=1)
        dec2 = self.dec2(cat2)
        drop2 = self.drop2(dec2)

        cat3 = torch.cat((drop2, enc6), dim=1)
        dec3 = self.dec3(cat3)
        drop3 = self.drop3(dec3)

        cat4 = torch.cat((drop3, enc5), dim=1)
        dec4 = self.dec4(cat4)

        cat5 = torch.cat((dec4, enc4), dim=1)
        dec5 = self.dec5(cat5)

        cat6 = torch.cat((dec5, enc3), dim=1)
        dec6 = self.dec6(cat6)

        cat7 = torch.cat((dec6, enc2), dim=1)
        dec7 = self.dec7(cat7)

        cat8 = torch.cat((dec7, enc1), dim=1)
        dec8 = self.dec8(cat8)

        x = torch.tanh(dec8)
        return x


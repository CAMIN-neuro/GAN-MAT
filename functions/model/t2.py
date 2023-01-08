from torch.utils.data import DataLoader
from torchvision import transforms

from model import *
from dataset import *


def test(args):
    pipeline_dir = args.pipeline_dir
    input_dir = args.input_dir
    batch_size = args.batch_size

    opts = [args.opts[0], np.asarray(args.opts[1:]).astype(np.float)]
    nch = args.nch
    nker = args.nker

    norm = args.norm

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    transform_ = transforms.Compose([Normalization(mean=0.5, std=0.5)])
    dataset_test = Dataset(input_dir=input_dir, transform=transform_, opts=opts)
    loader_test = DataLoader(dataset_test, batch_size=batch_size, shuffle=False, num_workers=8)

    netG = Pix2Pix_3D(in_channels=nch, out_channels=nch, nker=nker, norm=norm).to(device)
    dict_model = torch.load("{}/functions/model/model.pth".format(pipeline_dir), map_location=device)
    netG.load_state_dict(dict_model['netG'])

    with torch.no_grad():
        netG.eval()

        for batch, data in enumerate(loader_test, 1):
            input = data['input'].to(device)
            output = netG(input)

            for j in range(output.shape[0]):
                idx = batch_size * (batch - 1) + j
                output_ = output[j]
                output_ = output_.cpu().numpy()

                nifti = (output_[0] - output_[0].min()) / (output_[0].max() - output_[0].min())
                nib.save(nib.Nifti1Image(nifti, None),
                         input_dir + "/{}/output_T2w.nii.gz".format(dataset_test.lst_sub[idx]))

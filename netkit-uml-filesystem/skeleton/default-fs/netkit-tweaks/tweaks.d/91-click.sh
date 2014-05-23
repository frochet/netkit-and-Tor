#!/bin/sh
cat >> iclick.sh <<EOF
#!/bin/bash

cd /root/click
./configure --enable-local --disable-linuxmodule
cd userlevel
make -j5
make install
EOF
chmod +x iclick.sh

eval "${SUDO_PFX} cp -r ../../../click ${FS_MOUNT_DIR}/root/${SUDO_SFX}"
eval "${SUDO_PFX} cp iclick.sh  ${FS_MOUNT_DIR}/root/${SUDO_SFX}"
eval "${SUDO_PFX} chroot ${FS_MOUNT_DIR} /root/iclick.sh ${SUDO_SFX}"

rm -rf iclick.sh

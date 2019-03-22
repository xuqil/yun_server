## 项目云服务
备注：本项目采用Django2.1.4

#### 数据库结构

![](/screenshot/database.png)

1. auth_car
   - `uid` 主键，保存用户uid
   - `carid` 索引，车牌号
   - `appid` 外键连接auth_token,应用id
2. auth_app
   - `appid` 主键，应用id
   - `appsecred` 应用密码(本处出于简单处理，直接明文保存)
3. car_computed_data
   - `uid` 外键连接auth_car，上传用户uid
   - `gid` 索引，上传的分组
   - `data_record` 用户上传的实际运动值
   - `data_computed` 运算的理想运动值
   - `created` 上传保存的时间
4. car_data
   - `uid` 外键连接auth_car，上传用户uid
   - `gid` 索引，上传的分组
   - `g_sid` 索引，在某分组下的具体序号
   - `ccd` CCD 数组
   - `electric`  电感感应值
   - `acceleration`  加速度值
   - `speed`  速度编码值
   - `created` 上传保存的时间
5. car_image
   - `uid` 外键连接auth_car，上传用户uid
   - `gid` 索引，上传的分组
   - `g_sid` 索引，在某分组下的具体序号
   - `url` 主键，图片的url路径，命名方式为`/images_upload/{uid}_{gid}_{g_sid}_{created}`
   - `created` 图片上传保存时间
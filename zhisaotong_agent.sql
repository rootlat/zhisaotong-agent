/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80031 (8.0.31)
 Source Host           : localhost:3306
 Source Schema         : zhisaotong_agent

 Target Server Type    : MySQL
 Target Server Version : 80031 (8.0.31)
 File Encoding         : 65001

 Date: 11/05/2026 11:42:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chat_history
-- ----------------------------
DROP TABLE IF EXISTS `chat_history`;
CREATE TABLE `chat_history`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `session_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会话ID',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'user / assistant',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '内容',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_session`(`user_id` ASC, `session_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 208 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_history
-- ----------------------------
INSERT INTO `chat_history` VALUES (172, 1, '7236efc0-4e3c-40e3-bb4d-fb37f85ef0c2', 'user', '今天天气如何', '2026-05-07 12:35:44');
INSERT INTO `chat_history` VALUES (173, 1, '7236efc0-4e3c-40e3-bb4d-fb37f85ef0c2', 'assistant', '今天佛山市的天气情况如下：\n\n• 天气状况：多云\n• 气温：28摄氏度\n• 空气湿度：67%\n• 风向风力：南风，≤3级\n\n当前环境湿度适中，温度较高但无降雨，适合使用扫地机器人进行清洁。建议在室内使用扫拖一体机时，可适当开启除湿或通风，以提升清洁后地面干燥速度。', '2026-05-07 12:36:00');
INSERT INTO `chat_history` VALUES (174, 1, '3d58d162-70ae-44d1-95b1-216ccc91c627', 'user', '今天天气如何', '2026-05-07 12:39:13');
INSERT INTO `chat_history` VALUES (175, 1, '3d58d162-70ae-44d1-95b1-216ccc91c627', 'assistant', '佛山市今天天气为多云，气温28摄氏度，空气湿度67%，南风≤3级。\n\n\\n\n这样的天气条件对扫地机器人使用较为友好，湿度适中不会影响机器人的电子元件，地面也不会因为过于潮湿而影响清扫效果。建议您可以正常使用扫地机器人进行清洁工作。', '2026-05-07 12:39:25');
INSERT INTO `chat_history` VALUES (176, 1, '0c838064-9f55-4bfc-a92b-ef2c9da057af', 'user', '今天天气如何', '2026-05-07 12:40:15');
INSERT INTO `chat_history` VALUES (177, 1, '0c838064-9f55-4bfc-a92b-ef2c9da057af', 'assistant', '佛山市今天天气为多云，气温28摄氏度，空气湿度67%，南风≤3级。\n\n\\n\n这样的天气条件对扫地机器人使用较为友好，湿度适中不会影响机器人的电子元件，地面也不会因为过于潮湿而影响清扫效果。建议您可正常安排扫地机器人工作。', '2026-05-07 12:40:27');
INSERT INTO `chat_history` VALUES (178, 1, 'f69e6c24-cfa7-4da3-afde-48b53e50c457', 'user', '今天天气如何', '2026-05-07 12:45:09');
INSERT INTO `chat_history` VALUES (179, 1, 'f69e6c24-cfa7-4da3-afde-48b53e50c457', 'assistant', '佛山市今天天气为多云，气温28摄氏度，空气湿度67%，南风≤3级。\n\n\n\n这样的天气条件对扫地机器人使用较为友好，湿度适中不会影响机器人的电子元件，地面也不会过于潮湿。建议您可以在室内正常使用扫地机器人进行清洁工作。', '2026-05-07 12:45:21');
INSERT INTO `chat_history` VALUES (180, 1, '81554f6b-2bd7-4569-8684-a8bd758f78f4', 'user', '今天天气如何', '2026-05-07 12:46:51');
INSERT INTO `chat_history` VALUES (181, 1, '81554f6b-2bd7-4569-8684-a8bd758f78f4', 'assistant', '佛山市今天天气为多云，气温28摄氏度，空气湿度67%，南风≤3级。\n\n\\n\n这样的天气条件对扫地机器人的使用影响较小，您可以正常使用。不过由于湿度较高，建议在使用扫拖一体机时注意控制拖地水量，避免地面过于潮湿不易干燥。', '2026-05-07 12:47:02');
INSERT INTO `chat_history` VALUES (182, 1, '90f9723b-77a0-448d-b8af-d221eb69eb11', 'user', '今天天气如何', '2026-05-07 12:59:44');
INSERT INTO `chat_history` VALUES (183, 1, '90f9723b-77a0-448d-b8af-d221eb69eb11', 'assistant', '根据查询结果，今天佛山市的天气情况如下：\n\n- **天气状况**：多云  \n- **气温**：28℃  \n- **空气湿度**：67%  \n- **风向风力**：南风，≤3级  \n- **数据发布时间**：2026-05-07 12:31:10\n\n这样的天气对扫地机器人的使用影响较小，室内清洁可正常进行。不过若室外湿度较高，建议关注家中地面是否容易返潮，必要时可配合拖地功能或除湿设备使用。', '2026-05-07 12:59:58');
INSERT INTO `chat_history` VALUES (184, 1, '90f9723b-77a0-448d-b8af-d221eb69eb11', 'user', '机器人的清洁可怎么进行', '2026-05-07 13:02:25');
INSERT INTO `chat_history` VALUES (185, 1, '90f9723b-77a0-448d-b8af-d221eb69eb11', 'assistant', '机器人清洁需在装修后先手动清理尖锐杂物再使用；使用后及时清理主刷、尘盒，尤其在有宠物环境中；每周检查边刷、拆卸清洗主刷（非防水款用干布擦拭），晾干后安装；每月拆解吸口组件和检查拖地模组接口；清扫大颗粒垃圾或沾到宠物粪便后立即清理相关部件；集尘款更换集尘袋前关闭电源；尘盒有异味时用中性除味剂清洗，滤网发霉需更换；机身沾油污时用中性洗涤剂擦拭，并彻底清洗拖布。', '2026-05-07 13:02:33');
INSERT INTO `chat_history` VALUES (186, 1, '59fd26cd-e853-4a07-97f0-07331ad76446', 'user', '今天天气如何', '2026-05-07 13:08:11');
INSERT INTO `chat_history` VALUES (187, 1, '59fd26cd-e853-4a07-97f0-07331ad76446', 'assistant', '根据查询结果，今天佛山市的天气情况如下：\n\n- **天气状况**：多云  \n- **气温**：29℃  \n- **空气湿度**：66%  \n- **风向风力**：东南风，≤3级  \n- **数据发布时间**：2026-05-07 13:00:34\n\n这样的天气对扫地机器人的使用影响较小，湿度适中，地面不太可能因潮湿而影响清扫或拖地效果。如果您计划使用扫拖一体机进行湿拖，建议根据地板材质适当调整水量，避免因环境湿度较高导致干燥时间延长。', '2026-05-07 13:08:25');
INSERT INTO `chat_history` VALUES (188, 1, '59fd26cd-e853-4a07-97f0-07331ad76446', 'user', '机器人花了', '2026-05-07 13:08:38');
INSERT INTO `chat_history` VALUES (189, 1, '59fd26cd-e853-4a07-97f0-07331ad76446', 'assistant', '抱歉，关于“机器人花了”这一描述，目前未能在资料库中找到明确对应的解释或解决方案。\n\n请您确认一下具体是指以下哪种情况？以便我更准确地帮助您：\n\n- **机器人出现故障**（如无法启动、异常报错、不动等）？\n- **机器人卡住或被困**？\n- **购买机器人花费较高**，想了解性价比或优惠？\n- **屏幕显示异常**（如花屏、乱码）？\n- **其他问题**？\n\n欢迎补充更多细节！', '2026-05-07 13:08:55');
INSERT INTO `chat_history` VALUES (190, 1, '26a092f3-ab5e-45e9-86ea-11e4b506ac8c', 'user', '今天天气如何', '2026-05-07 13:10:47');
INSERT INTO `chat_history` VALUES (191, 1, '26a092f3-ab5e-45e9-86ea-11e4b506ac8c', 'assistant', '今天佛山的天气情况如下：\n\n- **天气状况**：多云\n- **气温**：29℃\n- **空气湿度**：66%\n- **风向风力**：东南风，≤3级\n- **数据发布时间**：2026-05-07 13:00:34\n\n这样的天气条件下，使用扫地机器人是完全没问题的。湿度适中，不会对机器人的电子元件造成影响，而且室内清洁效果也不会受到明显干扰。', '2026-05-07 13:11:03');
INSERT INTO `chat_history` VALUES (192, 1, '4fc4712c-d6f2-4066-acc3-9199ec76a363', 'user', '今天天气如何', '2026-05-07 13:11:37');
INSERT INTO `chat_history` VALUES (193, 1, '4fc4712c-d6f2-4066-acc3-9199ec76a363', 'assistant', '根据查询结果，今天佛山市的天气情况如下：\n\n- **天气状况**：多云  \n- **气温**：29℃  \n- **空气湿度**：66%  \n- **风向风力**：东南风，≤3级  \n- **数据发布时间**：2026-05-07 13:00:34  \n\n这样的天气对扫地机器人的使用影响较小，湿度适中，地面不易过于潮湿或干燥，适合正常清扫。如果您的扫拖一体机计划进行拖地，请注意适当控制水量，避免因环境湿度较高导致地面干得较慢。', '2026-05-07 13:11:53');
INSERT INTO `chat_history` VALUES (194, 1, 'c7913d53-6a52-46a0-bb55-c696d8e6c817', 'user', '今天天气如何', '2026-05-07 13:14:07');
INSERT INTO `chat_history` VALUES (195, 1, 'c7913d53-6a52-46a0-bb55-c696d8e6c817', 'assistant', '今天佛山的天气情况如下：\n\n- **天气状况**：多云\n- **气温**：29℃\n- **空气湿度**：66%\n- **风向风力**：东南风，≤3级\n- **数据发布时间**：2026-05-07 13:00:34\n\n这样的天气条件下，适合使用扫地机器人进行清洁工作。湿度适中，不会对机器人的电子元件造成影响，而且室内地面不太可能有明显潮湿问题。', '2026-05-07 13:14:20');
INSERT INTO `chat_history` VALUES (196, 1, '0db247f6-a1c9-46e7-a151-9931ec8032ba', 'user', '今天天气如何', '2026-05-07 13:15:23');
INSERT INTO `chat_history` VALUES (197, 1, '0db247f6-a1c9-46e7-a151-9931ec8032ba', 'assistant', '今天佛山市的天气情况如下：\n\n- **天气状况**：多云  \n- **气温**：29℃  \n- **空气湿度**：66%  \n- **风向风力**：东南风，≤3级  \n- **数据发布时间**：2026-05-07 13:00:34\n\n这样的天气对扫地机器人的使用影响较小，湿度适中，地面不易过于潮湿或干燥，适合正常清扫。如果您使用的是扫拖一体机器人，建议根据室内地面实际情况调整拖地水量，避免因环境湿度较高导致地面干燥较慢。', '2026-05-07 13:15:39');
INSERT INTO `chat_history` VALUES (198, 1, 'd3e65239-dbf2-46fb-8285-1d81667fda6d', 'user', '今天天气如何', '2026-05-07 13:18:14');
INSERT INTO `chat_history` VALUES (199, 1, 'd3e65239-dbf2-46fb-8285-1d81667fda6d', 'assistant', '今天佛山市的天气情况如下：\n\n- 天气状况：多云\n- 气温：29℃\n- 空气湿度：66%\n- 风向风力：东南风，≤3级\n- 数据发布时间：2026-05-07 13:00:34\n\n这样的天气条件对扫地机器人使用比较友好，湿度适中，没有降雨，地面干燥，适合进行清扫和拖地任务。', '2026-05-07 13:18:25');
INSERT INTO `chat_history` VALUES (200, 1, 'f81fbb55-4ed2-4d77-afb9-d8ce253306db', 'user', '今天天气如何', '2026-05-07 13:19:36');
INSERT INTO `chat_history` VALUES (201, 1, 'f81fbb55-4ed2-4d77-afb9-d8ce253306db', 'assistant', '今天佛山市的天气情况如下：\n\n- 天气：多云\n- 气温：29℃\n- 空气湿度：66%\n- 风向风力：东南风，≤3级\n- 数据发布时间：2026-05-07 13:00:34\n\n当前天气较为温暖湿润，适合使用扫地机器人进行清洁。较高的湿度可能使地面略显潮湿，建议在使用扫拖一体机时适当调整水量，避免地板过湿。', '2026-05-07 13:19:50');
INSERT INTO `chat_history` VALUES (202, 1, 'd0f69e91-7cd5-4847-9868-6a5d9a448cc0', 'user', '今天天气如何', '2026-05-07 13:21:35');
INSERT INTO `chat_history` VALUES (203, 1, 'd0f69e91-7cd5-4847-9868-6a5d9a448cc0', 'assistant', '今天佛山的天气情况如下：\n\n- 天气状况：多云\n- 气温：29℃\n- 空气湿度：66%\n- 风向风力：东南风，≤3级\n\n这样的天气条件对扫地机器人使用较为友好，湿度适中，不会因过于潮湿影响机器人的电子元件，也不会因过于干燥导致灰尘飞扬难以清理。建议您可以在室内正常使用扫地机器人进行清洁。', '2026-05-07 13:21:49');
INSERT INTO `chat_history` VALUES (204, 1, 'cb5b3f31-b8fb-4e0c-bfd1-3fec18d9a643', 'user', '今天天气如何', '2026-05-07 13:24:38');
INSERT INTO `chat_history` VALUES (205, 1, 'cb5b3f31-b8fb-4e0c-bfd1-3fec18d9a643', 'assistant', '今天佛山市的天气情况如下：\n\n- **天气状况**：多云  \n- **气温**：29℃  \n- **空气湿度**：66%  \n- **风向风力**：东南风，≤3级  \n- **数据发布时间**：2026-05-07 13:00:34\n\n这样的天气对扫地机器人使用影响较小，室内清洁可正常进行。不过由于湿度较高，若使用扫拖一体机，建议适当减少拖地水量，避免地面干燥慢或产生水渍。', '2026-05-07 13:24:52');
INSERT INTO `chat_history` VALUES (206, 1, '7365aee1-6d32-41a1-b169-7672accac15d', 'user', '今天天气如何', '2026-05-07 13:28:39');
INSERT INTO `chat_history` VALUES (207, 1, '7365aee1-6d32-41a1-b169-7672accac15d', 'assistant', '今天佛山市的天气情况如下：\n\n- 天气：多云  \n- 气温：29℃  \n- 空气湿度：66%  \n- 风向风力：东南风，≤3级  \n\n这样的天气对扫地机器人的使用影响较小，室内清洁可正常进行。不过若开窗通风，较高湿度可能使地面略显潮气，建议扫拖一体机的拖地功能根据地面实际情况酌情使用。', '2026-05-07 13:28:52');

-- ----------------------------
-- Table structure for file
-- ----------------------------
DROP TABLE IF EXISTS `file`;
CREATE TABLE `file`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '文件ID',
  `fileName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件名',
  `fileSize` double NOT NULL COMMENT '文件大小（KB）',
  `filePath` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件存储路径',
  `fileMd5` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件MD5值（用于去重）',
  `userId` int NOT NULL COMMENT '上传用户ID',
  `status` int NOT NULL DEFAULT 1 COMMENT '状态 1—已上传（待解析）2—解析中 3—解析成功 4—解析失败',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`userId` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 50 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '文件管理表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of file
-- ----------------------------
INSERT INTO `file` VALUES (43, '扫地机器人100问.pdf', 192676, 'D:\\PyCharm\\Project\\AI\\RAG+Agent\\智扫通机器人智能客服\\zhisaotong-agent\\data\\扫地机器人100问.pdf', '6d726f4604d9e7ebcf59a932ae9e9c00', 0, 3, '2026-05-05 13:14:45', '2026-05-05 13:14:45');
INSERT INTO `file` VALUES (44, '扫地机器人100问2.txt', 18306, 'D:\\PyCharm\\Project\\AI\\RAG+Agent\\智扫通机器人智能客服\\zhisaotong-agent\\data\\扫地机器人100问2.txt', 'a29a4ba5a539a2a462def8f91eb98ccc', 0, 3, '2026-05-05 13:14:45', '2026-05-05 13:14:45');
INSERT INTO `file` VALUES (45, '扫拖一体机器人100问.txt', 21128, 'D:\\PyCharm\\Project\\AI\\RAG+Agent\\智扫通机器人智能客服\\zhisaotong-agent\\data\\扫拖一体机器人100问.txt', 'd294281a5769e0a3d1455fbf637ee572', 0, 3, '2026-05-05 13:14:45', '2026-05-05 13:14:45');
INSERT INTO `file` VALUES (46, '故障排除.txt', 42138, 'D:\\PyCharm\\Project\\AI\\RAG+Agent\\智扫通机器人智能客服\\zhisaotong-agent\\data\\故障排除.txt', '928c24dbdeeb1c0a109f5620c8bac429', 0, 3, '2026-05-05 13:14:45', '2026-05-05 13:14:45');
INSERT INTO `file` VALUES (47, '维护保养.txt', 24309, 'D:\\PyCharm\\Project\\AI\\RAG+Agent\\智扫通机器人智能客服\\zhisaotong-agent\\data\\维护保养.txt', 'fc539588792a89ff842cf241cf822de1', 0, 3, '2026-05-05 13:14:45', '2026-05-05 13:14:45');
INSERT INTO `file` VALUES (48, '选购指南.txt', 22364, 'D:\\PyCharm\\Project\\AI\\RAG+Agent\\智扫通机器人智能客服\\zhisaotong-agent\\data\\选购指南.txt', '94bd6c0b4283b8524f4e8dfc5b72f8ab', 0, 3, '2026-05-05 13:14:45', '2026-05-05 13:14:45');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '1正常 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `uk_phone`(`phone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '张三', '18674594562', '$2b$12$rsWeG8jkPj5FjWClPU6rKe4n6Nk9Wua8o7hvHZqZudv00JkIGh9U.', 1, '2026-05-05 10:24:28', '2026-05-05 10:24:28');

-- ----------------------------
-- Table structure for user_token
-- ----------------------------
DROP TABLE IF EXISTS `user_token`;
CREATE TABLE `user_token`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '令牌ID',
  `user_id` int UNSIGNED NOT NULL COMMENT '用户ID',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '令牌值',
  `expires_at` timestamp NOT NULL COMMENT '过期时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户令牌表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_token
-- ----------------------------
INSERT INTO `user_token` VALUES (1, 1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc4NzM2NTEyfQ.1LPHfCcAzeBk5XJJSzWHy-MvkmCkK5veVzwW-JnnIxU', '2026-05-14 13:28:33', '2026-05-05 10:24:28');

SET FOREIGN_KEY_CHECKS = 1;

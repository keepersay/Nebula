from .base import BaseQueryConfig, FieldConfig, FieldType, BaseQuery

class ServerQueryConfig(BaseQueryConfig):
    """服务器查询配置"""
    def __init__(self):
        super().__init__()
        self._init_fields()
    
    def _init_fields(self):
        """初始化字段配置"""
        # ID字段
        self.add_field("id", FieldConfig(
            name="id",
            type=FieldType.INTEGER,
            description="服务器ID",
            operators=["=", "!=", "in"]
        ))
        
        # 基本信息字段
        self.add_field("service_tag", FieldConfig(
            name="service_tag",
            type=FieldType.STRING,
            description="设备序列号",
            operators=["=", "!=", "like", "in"]
        ))
        
        self.add_field("name", FieldConfig(
            name="name",
            type=FieldType.STRING,
            description="服务器名称",
            operators=["=", "!=", "like", "in"]
        ))
        
        self.add_field("description", FieldConfig(
            name="description",
            type=FieldType.STRING,
            description="服务器描述",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("agent_name", FieldConfig(
            name="agent_name",
            type=FieldType.STRING,
            description="Agent抓取主机名",
            operators=["=", "!=", "like", "in"]
        ))
        
        # IP信息
        self.add_field("primary_ip", FieldConfig(
            name="primary_ip",
            type=FieldType.STRING,
            description="主IP",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("agent_ip", FieldConfig(
            name="agent_ip",
            type=FieldType.STRING,
            description="Agent抓取ip",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("other_ip", FieldConfig(
            name="other_ip",
            type=FieldType.STRING,
            description="其他ip地址",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("port", FieldConfig(
            name="port",
            type=FieldType.STRING,
            description="docker端口",
            operators=["=", "!=", "like", "in"]
        ))

        # 管理卡信息
        self.add_field("manage_card_ip", FieldConfig(
            name="manage_card_ip",
            type=FieldType.STRING,
            description="管理卡IP地址",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("manage_card_mac", FieldConfig(
            name="manage_card_mac",
            type=FieldType.STRING,
            description="管理卡MAC地址",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("manage_card_version", FieldConfig(
            name="manage_card_version",
            type=FieldType.STRING,
            description="管理卡固件版本",
            operators=["=", "!=", "like", "in"]
        ))

        # 系统信息
        self.add_field("bios_version", FieldConfig(
            name="bios_version",
            type=FieldType.STRING,
            description="BIOS版本号",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("raid_fw_version", FieldConfig(
            name="raid_fw_version",
            type=FieldType.STRING,
            description="RAID卡固件版本",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("agent_version", FieldConfig(
            name="agent_version",
            type=FieldType.STRING,
            description="Agent版本",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("agent_kernel", FieldConfig(
            name="agent_kernel",
            type=FieldType.STRING,
            description="agent内核",
            operators=["=", "!=", "like", "in"]
        ))
        
        # 状态字段
        self.add_field("is_valid", FieldConfig(
            name="is_valid",
            type=FieldType.BOOLEAN,
            description="是否有效",
            operators=["=", "!="]
        ))
        
        self.add_field("use_status", FieldConfig(
            name="use_status",
            type=FieldType.ENUM,
            description="使用状态",
            operators=["=", "!=", "in"],
            enum_values=["ready", "in_use", "maintenance"]
        ))

        self.add_field("service_level", FieldConfig(
            name="service_level",
            type=FieldType.INTEGER,
            description="服务级别",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("is_installing", FieldConfig(
            name="is_installing",
            type=FieldType.INTEGER,
            description="是否正在安装",
            operators=["=", "!=", "in"]
        ))

        self.add_field("install_status", FieldConfig(
            name="install_status",
            type=FieldType.ENUM,
            description="装机状态",
            operators=["=", "!=", "in"],
            enum_values=["uninstall", "installing", "installed", "failed"]
        ))

        self.add_field("lock_status", FieldConfig(
            name="lock_status",
            type=FieldType.ENUM,
            description="锁状态",
            operators=["=", "!=", "in"],
            enum_values=["unlocked", "locked"]
        ))
        
        # 时间字段
        self.add_field("created_date", FieldConfig(
            name="created_date",
            type=FieldType.DATETIME,
            description="创建时间",
            operators=["=", "!=", ">", "<", ">=", "<="]
        ))
        
        # 关联字段
        self.add_field("network_segment_id", FieldConfig(
            name="network_segment_id",
            type=FieldType.INTEGER,
            description="网段ID",
            operators=["=", "!=", "in"],
            is_multi_select=True
        ))

        # 虚拟机信息
        self.add_field("is_vm", FieldConfig(
            name="is_vm",
            type=FieldType.INTEGER,
            description="是否虚拟机",
            operators=["=", "!=", "in"]
        ))

        self.add_field("real_server_id", FieldConfig(
            name="real_server_id",
            type=FieldType.INTEGER,
            description="宿主机id",
            operators=["=", "!=", "in"]
        ))

        self.add_field("vm_type", FieldConfig(
            name="vm_type",
            type=FieldType.ENUM,
            description="虚拟机类型",
            operators=["=", "!=", "in"],
            enum_values=["undefined", "kvm", "vmware", "docker"]
        ))

        self.add_field("vm_network_type", FieldConfig(
            name="vm_network_type",
            type=FieldType.ENUM,
            description="虚拟机网络类型",
            operators=["=", "!=", "in"],
            enum_values=["undefined", "bridge", "nat", "host"]
        ))

        self.add_field("instance_name", FieldConfig(
            name="instance_name",
            type=FieldType.STRING,
            description="实例名称",
            operators=["=", "!=", "like", "in"]
        ))

        # 硬件信息
        self.add_field("cpu_amount", FieldConfig(
            name="cpu_amount",
            type=FieldType.INTEGER,
            description="CPU数量",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("cpu_cores", FieldConfig(
            name="cpu_cores",
            type=FieldType.INTEGER,
            description="CPU物理核总数",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("cpu_kernel_number", FieldConfig(
            name="cpu_kernel_number",
            type=FieldType.FLOAT,
            description="CPU线程总数",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("ram_amount", FieldConfig(
            name="ram_amount",
            type=FieldType.INTEGER,
            description="内存数量",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("ram_size", FieldConfig(
            name="ram_size",
            type=FieldType.FLOAT,
            description="内存大小,单位G",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("nic_amount", FieldConfig(
            name="nic_amount",
            type=FieldType.INTEGER,
            description="网卡数量",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("storage_amount", FieldConfig(
            name="storage_amount",
            type=FieldType.INTEGER,
            description="硬盘数量",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        self.add_field("storage_info", FieldConfig(
            name="storage_info",
            type=FieldType.STRING,
            description="存储配置",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("filesystem_disk_space", FieldConfig(
            name="filesystem_disk_space",
            type=FieldType.INTEGER,
            description="系统磁盘空间",
            operators=["=", "!=", ">", "<", ">=", "<=", "in"]
        ))

        # 其他关联ID
        self.add_field("device_id", FieldConfig(
            name="device_id",
            type=FieldType.INTEGER,
            description="设备ID",
            operators=["=", "!=", "in"]
        ))

        self.add_field("group_id", FieldConfig(
            name="group_id",
            type=FieldType.INTEGER,
            description="分组ID",
            operators=["=", "!=", "in"]
        ))

        self.add_field("agent_os_id", FieldConfig(
            name="agent_os_id",
            type=FieldType.INTEGER,
            description="agent采集的操作系统ID",
            operators=["=", "!=", "in"]
        ))

        self.add_field("template_id", FieldConfig(
            name="template_id",
            type=FieldType.INTEGER,
            description="装机模板ID",
            operators=["=", "!=", "in"]
        ))

        self.add_field("image_id", FieldConfig(
            name="image_id",
            type=FieldType.INTEGER,
            description="镜像ID",
            operators=["=", "!=", "in"]
        ))

        # 其他信息
        self.add_field("owner", FieldConfig(
            name="owner",
            type=FieldType.STRING,
            description="服务器使用人",
            operators=["=", "!=", "like", "in"]
        ))

        self.add_field("label", FieldConfig(
            name="label",
            type=FieldType.STRING,
            description="服务器标签",
            operators=["=", "!=", "like", "in"]
        ))

# 创建服务器查询配置实例
SERVER_QUERY_CONFIG = ServerQueryConfig() 
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ConflictError(Exception):
    """资源冲突异常"""
    pass

class ServerBase(BaseModel):
    """服务器基本信息"""
    # 必填字段
    network_segment_id: int = Field(description="网段ID")
    service_tag: str = Field(description="设备序列号")

    # name字段
    name: Optional[str] = Field(default="", description="服务器名")
    agent_name: Optional[str] = Field(default="", description="Agent抓取主机名")
    
    # IP信息
    primary_ip: Optional[str] = Field(default="", description="主IP")
    agent_ip: Optional[str] = Field(default="", description="Agent抓取ip")
    other_ip: Optional[str] = Field(default="", description="其他ip地址")
    port: Optional[str] = Field(default="", description="docker端口")

    # 管理卡信息
    manage_card_ip: Optional[str] = Field(default="", description="管理卡IP地址")
    manage_card_mac: Optional[str] = Field(default="", description="管理卡MAC地址")
    manage_card_version: Optional[str] = Field(default="", description="管理卡固件版本")

    # 系统信息
    bios_version: Optional[str] = Field(default="", description="BIOS版本号")
    raid_fw_version: Optional[str] = Field(default="", description="RAID卡固件版本")
    agent_version: Optional[str] = Field(default="", description="Agent版本")
    agent_kernel: Optional[str] = Field(default="", description="agent内核")

    # 状态信息
    use_status: Optional[str] = Field(default="ready", description="使用状态")
    service_level: Optional[int] = Field(default=0, description="服务级别")
    is_installing: Optional[int] = Field(default=0, description="是否正在安装")
    install_status: Optional[str] = Field(default="uninstall", description="装机状态")
    lock_status: Optional[str] = Field(default="unlocked", description="锁状态")

    # 虚拟机信息
    is_vm: Optional[int] = Field(default=0, description="是否虚拟机")
    real_server_id: Optional[int] = Field(default=0, description="宿主机id")
    vm_type: Optional[str] = Field(default="undefined", description="虚拟机类型")
    vm_network_type: Optional[str] = Field(default="undefined", description="虚拟机网络类型")
    instance_name: Optional[str] = Field(default="", description="实例名称")

    # 硬件信息
    cpu_amount: Optional[int] = Field(default=0, description="CPU数量")
    cpu_cores: Optional[int] = Field(default=0, description="CPU物理核总数")
    cpu_kernel_number: Optional[float] = Field(default=0.00, description="CPU线程总数")
    ram_amount: Optional[int] = Field(default=0, description="内存数量")
    ram_size: Optional[float] = Field(default=0.00, description="内存大小,单位G")
    nic_amount: Optional[int] = Field(default=0, description="网卡数量")
    storage_amount: Optional[int] = Field(default=0, description="硬盘数量")
    storage_info: Optional[str] = Field(default="", description="存储配置")
    filesystem_disk_space: Optional[int] = Field(default=0, description="系统磁盘空间")

    # 关联ID
    device_id: Optional[int] = Field(default=0, description="设备ID")
    group_id: Optional[int] = Field(default=0, description="分组ID")
    agent_os_id: Optional[int] = Field(default=0, description="agent采集的操作系统ID")
    template_id: Optional[int] = Field(default=0, description="装机模板ID")
    image_id: Optional[int] = Field(default=0, description="镜像ID")

    # 其他信息
    owner: Optional[str] = Field(default="", description="服务器使用人")
    label: Optional[str] = Field(default="", description="服务器归属")
    description: str = Field(default="", description="描述")

class ServerCreate(ServerBase):
    """创建服务器时的请求数据"""
    network_segment_id: Optional[int] = None

class ServerUpdate(BaseModel):
    """更新服务器时的请求数据"""
    network_segment_id: Optional[int] = None
    service_tag: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    agent_name: Optional[str] = None
    primary_ip: Optional[str] = None
    agent_ip: Optional[str] = None
    other_ip: Optional[str] = None
    port: Optional[str] = None
    manage_card_ip: Optional[str] = None
    manage_card_mac: Optional[str] = None
    manage_card_version: Optional[str] = None
    bios_version: Optional[str] = None
    raid_fw_version: Optional[str] = None
    agent_version: Optional[str] = None
    agent_kernel: Optional[str] = None
    use_status: Optional[str] = None
    service_level: Optional[int] = None
    is_installing: Optional[int] = None
    install_status: Optional[str] = None
    lock_status: Optional[str] = None
    is_vm: Optional[int] = None
    real_server_id: Optional[int] = None
    vm_type: Optional[str] = None
    vm_network_type: Optional[str] = None
    instance_name: Optional[str] = None
    cpu_amount: Optional[int] = None
    cpu_cores: Optional[int] = None
    cpu_kernel_number: Optional[float] = None
    ram_amount: Optional[int] = None
    ram_size: Optional[float] = None
    nic_amount: Optional[int] = None
    storage_amount: Optional[int] = None
    storage_info: Optional[str] = None
    filesystem_disk_space: Optional[int] = None
    device_id: Optional[int] = None
    group_id: Optional[int] = None
    agent_os_id: Optional[int] = None
    template_id: Optional[int] = None
    image_id: Optional[int] = None
    owner: Optional[str] = None
    label: Optional[str] = None

class Server(ServerBase):
    """服务器响应数据"""
    id: int
    created_by: str
    created_date: datetime
    last_modified_by: str
    last_modified_date: datetime

    class Config:
        from_attributes = True

 
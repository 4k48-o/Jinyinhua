/**
 * 角色创建/编辑表单
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Modal, Form, Input, InputNumber, Switch, message, Space, Button, Row, Col, Divider } from 'antd'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { createRole, updateRole, fetchPermissionTree } from '@/store/slices/roleSlice'
import { useDebounceFn } from '@/hooks/useDebounce'
import { getRolePermissions } from '@/api/role'
import type { RoleListItem, CreateRoleRequest, UpdateRoleRequest } from '@/types/role'
import PermissionTreeSelector from './PermissionTreeSelector'

interface RoleFormProps {
  visible: boolean
  role: RoleListItem | null
  onClose: () => void
  onSuccess: () => void
}

const RoleForm = ({ visible, role, onClose, onSuccess }: RoleFormProps) => {
  const { t } = useTranslation()
  const dispatch = useAppDispatch()
  const { permissionTree, permissionTreeLoading } = useAppSelector((state) => state.role)
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [selectedPermissionIds, setSelectedPermissionIds] = useState<number[]>([])

  // 加载角色权限
  const loadRolePermissions = async (roleId: number) => {
    try {
      const permissions = await getRolePermissions(roleId)
      setSelectedPermissionIds(permissions.map((p) => p.id))
    } catch (error: any) {
      message.error(error.message || '加载角色权限失败')
    }
  }

  // 初始化表单
  useEffect(() => {
    if (visible) {
      if (role) {
        // 编辑模式：加载角色详情和权限
        form.setFieldsValue({
          name: role.name,
          code: role.code,
          description: role.description,
          sort_order: role.sort_order,
          is_active: role.is_active,
        })
        // 加载角色的权限列表
        loadRolePermissions(role.id)
      } else {
        // 创建模式：重置表单
        form.resetFields()
        setSelectedPermissionIds([])
      }
      
      // 加载权限树
      if (permissionTree.length === 0) {
        dispatch(fetchPermissionTree())
      }
    }
  }, [visible, role, form, dispatch, permissionTree.length])

  // 处理提交（实际执行函数）
  const executeSubmit = async () => {
    try {
      const values = await form.validateFields()
      setLoading(true)

      const formData: CreateRoleRequest | UpdateRoleRequest = {
        ...values,
        permission_ids: selectedPermissionIds,
      }

      if (role) {
        // 更新角色
        await dispatch(updateRole({ id: role.id, data: formData })).unwrap()
      } else {
        // 创建角色
        await dispatch(createRole(formData as CreateRoleRequest)).unwrap()
      }

      onSuccess()
    } catch (error: any) {
      if (error?.errorFields) {
        // 表单验证错误
        return
      }
      // 其他错误已在 slice 中处理
    } finally {
      setLoading(false)
    }
  }

  // 防抖处理提交（防止重复点击）
  const handleSubmitDebounced = useDebounceFn(executeSubmit, 500)

  const handleSubmit = () => {
    // 如果正在加载，不执行（防止重复提交）
    if (loading) {
      return
    }
    // 使用防抖，防止快速连续点击
    handleSubmitDebounced()
  }

  // 处理取消
  const handleCancel = () => {
    form.resetFields()
    setSelectedPermissionIds([])
    onClose()
  }

  return (
    <Modal
      title={role ? (t('role.edit') || '编辑角色') : (t('role.create') || '创建角色')}
      open={visible}
      onCancel={handleCancel}
      onOk={handleSubmit}
      confirmLoading={loading}
      width={1200}
      destroyOnClose
    >
      <Row gutter={24}>
        {/* 左侧：编辑表单 */}
        <Col span={12}>
          <Form
            form={form}
            layout="vertical"
            initialValues={{
              sort_order: 0,
              is_active: true,
            }}
          >
            <Form.Item
              name="name"
              label={t('role.name') || '角色名称'}
              rules={[
                { required: true, message: t('role.nameRequired') || '请输入角色名称' },
                { max: 50, message: t('role.nameMaxLength') || '角色名称不能超过50个字符' },
              ]}
            >
              <Input placeholder={t('role.namePlaceholder') || '请输入角色名称'} />
            </Form.Item>

            <Form.Item
              name="code"
              label={t('role.code') || '角色代码'}
              rules={[
                { required: true, message: t('role.codeRequired') || '请输入角色代码' },
                { pattern: /^[a-z0-9_]+$/, message: t('role.codePattern') || '角色代码只能包含小写字母、数字和下划线' },
                { max: 50, message: t('role.codeMaxLength') || '角色代码不能超过50个字符' },
              ]}
            >
              <Input placeholder={t('role.codePlaceholder') || '请输入角色代码，如：admin'} disabled={!!role} />
            </Form.Item>

            <Form.Item
              name="description"
              label={t('role.description') || '描述'}
              rules={[
                { max: 500, message: t('role.descriptionMaxLength') || '描述不能超过500个字符' },
              ]}
            >
              <Input.TextArea
                rows={4}
                placeholder={t('role.descriptionPlaceholder') || '请输入角色描述'}
              />
            </Form.Item>

            <Form.Item
              name="sort_order"
              label={t('role.sortOrder') || '排序顺序'}
              rules={[
                { type: 'number', min: 0, message: t('role.sortOrderMin') || '排序顺序不能小于0' },
              ]}
            >
              <InputNumber
                min={0}
                style={{ width: '100%' }}
                placeholder={t('role.sortOrderPlaceholder') || '请输入排序顺序'}
              />
            </Form.Item>

            <Form.Item
              name="is_active"
              label={t('role.status') || '状态'}
              valuePropName="checked"
            >
              <Switch
                checkedChildren={t('common.active') || '激活'}
                unCheckedChildren={t('common.inactive') || '禁用'}
              />
            </Form.Item>
          </Form>
        </Col>

        {/* 右侧：权限树 */}
        <Col span={12}>
          <div>
            <div style={{ marginBottom: 8, fontWeight: 500 }}>
              {t('role.permissions') || '权限'} <span style={{ color: '#ff4d4f' }}>*</span>
            </div>
            <PermissionTreeSelector
              treeData={permissionTree}
              loading={permissionTreeLoading}
              value={selectedPermissionIds}
              onChange={setSelectedPermissionIds}
            />
          </div>
        </Col>
      </Row>
    </Modal>
  )
}

export default RoleForm


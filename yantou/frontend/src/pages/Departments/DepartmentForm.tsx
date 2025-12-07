/**
 * 部门创建/编辑表单
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Modal, Form, Input, InputNumber, Switch, Select, message } from 'antd'
import { createDepartment, updateDepartment, getDepartmentList } from '@/api/department'
import { useDebounceFn } from '@/hooks/useDebounce'
import type { DepartmentListItem, CreateDepartmentRequest, UpdateDepartmentRequest } from '@/types/department'
import { get } from '@/utils/request'
import type { User, PaginatedResponse } from '@/types'

interface DepartmentFormProps {
  visible: boolean
  department: DepartmentListItem | null
  onClose: () => void
  onSuccess: () => void
}

const DepartmentForm = ({ visible, department, onClose, onSuccess }: DepartmentFormProps) => {
  const { t } = useTranslation()
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [parentOptions, setParentOptions] = useState<Array<{ label: string; value: number }>>([])
  const [managerOptions, setManagerOptions] = useState<Array<{ label: string; value: number }>>([])
  const [loadingParents, setLoadingParents] = useState(false)
  const [loadingManagers, setLoadingManagers] = useState(false)

  // 加载父部门选项
  const loadParentOptions = async () => {
    setLoadingParents(true)
    try {
      const response = await getDepartmentList({ page_size: 1000, is_active: true })
      const options = response.results
        .filter((dept) => !department || dept.id !== department.id) // 排除自己
        .map((dept) => ({
          label: dept.name,
          value: dept.id,
        }))
      setParentOptions([{ label: t('department.noParent') || '无（顶级部门）', value: 0 }, ...options])
    } catch (error: any) {
      message.error(error.message || '加载父部门列表失败')
    } finally {
      setLoadingParents(false)
    }
  }

  // 加载负责人选项
  const loadManagerOptions = async () => {
    setLoadingManagers(true)
    try {
      const response = await get<PaginatedResponse<User>>('/users/', { page_size: 1000, is_active: true })
      const options = response.results.map((user) => ({
        label: user.username,
        value: user.id,
      }))
      setManagerOptions([{ label: t('department.noManager') || '无', value: 0 }, ...options])
    } catch (error: any) {
      message.error(error.message || '加载用户列表失败')
    } finally {
      setLoadingManagers(false)
    }
  }

  // 初始化表单
  useEffect(() => {
    if (visible) {
      if (department) {
        // 编辑模式
        form.setFieldsValue({
          name: department.name,
          code: department.code,
          parent: department.parent || 0,
          manager: department.manager || 0,
          description: department.description,
          sort_order: department.sort_order,
          is_active: department.is_active,
        })
      } else {
        // 创建模式
        form.resetFields()
        form.setFieldsValue({
          parent: 0,
          manager: 0,
          sort_order: 0,
          is_active: true,
        })
      }
      
      // 加载选项
      loadParentOptions()
      loadManagerOptions()
    }
  }, [visible, department, form])

  // 处理提交（实际执行函数）
  const executeSubmit = async () => {
    try {
      const values = await form.validateFields()
      setLoading(true)

      const formData: CreateDepartmentRequest | UpdateDepartmentRequest = {
        name: values.name,
        code: values.code || undefined,
        parent: values.parent === 0 ? null : values.parent,
        manager: values.manager === 0 ? null : values.manager,
        description: values.description,
        sort_order: values.sort_order || 0,
        is_active: values.is_active !== undefined ? values.is_active : true,
      }

      if (department) {
        // 更新部门
        await updateDepartment(department.id, formData)
        message.success(t('department.updateSuccess') || '部门更新成功')
      } else {
        // 创建部门
        await createDepartment(formData as CreateDepartmentRequest)
        message.success(t('department.createSuccess') || '部门创建成功')
      }

      onSuccess()
    } catch (error: any) {
      if (error?.errorFields) {
        // 表单验证错误
        return
      }
      message.error(error.message || (department ? '更新部门失败' : '创建部门失败'))
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
    onClose()
  }

  return (
    <Modal
      title={department ? (t('department.edit') || '编辑部门') : (t('department.create') || '创建部门')}
      open={visible}
      onOk={handleSubmit}
      onCancel={handleCancel}
      confirmLoading={loading}
      width={600}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          parent: 0,
          manager: 0,
          sort_order: 0,
          is_active: true,
        }}
      >
        <Form.Item
          name="name"
          label={t('department.name') || '部门名称'}
          rules={[
            { required: true, message: t('department.nameRequired') || '请输入部门名称' },
            { max: 100, message: t('department.nameMaxLength') || '部门名称不能超过100个字符' },
          ]}
        >
          <Input placeholder={t('department.namePlaceholder') || '请输入部门名称'} />
        </Form.Item>

        <Form.Item
          name="code"
          label={t('department.code') || '部门代码'}
          rules={[
            { max: 50, message: t('department.codeMaxLength') || '部门代码不能超过50个字符' },
            { pattern: /^[a-z0-9_]+$/, message: t('department.codePattern') || '部门代码只能包含小写字母、数字和下划线' },
          ]}
        >
          <Input placeholder={t('department.codePlaceholder') || '请输入部门代码（可选）'} />
        </Form.Item>

        <Form.Item
          name="parent"
          label={t('department.parent') || '父部门'}
        >
          <Select
            placeholder={t('department.parentPlaceholder') || '请选择父部门'}
            loading={loadingParents}
            allowClear
            showSearch
            filterOption={(input, option) =>
              (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
            }
            options={parentOptions}
          />
        </Form.Item>

        <Form.Item
          name="manager"
          label={t('department.manager') || '负责人'}
        >
          <Select
            placeholder={t('department.managerPlaceholder') || '请选择负责人'}
            loading={loadingManagers}
            allowClear
            showSearch
            filterOption={(input, option) =>
              (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
            }
            options={managerOptions}
          />
        </Form.Item>

        <Form.Item
          name="description"
          label={t('department.description') || '描述'}
          rules={[
            { max: 500, message: t('department.descriptionMaxLength') || '描述不能超过500个字符' },
          ]}
        >
          <Input.TextArea
            rows={3}
            placeholder={t('department.descriptionPlaceholder') || '请输入部门描述'}
          />
        </Form.Item>

        <Form.Item
          name="sort_order"
          label={t('department.sortOrder') || '排序顺序'}
          rules={[
            { type: 'number', min: 0, message: t('department.sortOrderMin') || '排序顺序不能小于0' },
          ]}
        >
          <InputNumber
            style={{ width: '100%' }}
            placeholder={t('department.sortOrderPlaceholder') || '请输入排序顺序'}
            min={0}
          />
        </Form.Item>

        <Form.Item
          name="is_active"
          label={t('department.status') || '状态'}
          valuePropName="checked"
        >
          <Switch checkedChildren={t('common.active') || '激活'} unCheckedChildren={t('common.inactive') || '禁用'} />
        </Form.Item>
      </Form>
    </Modal>
  )
}

export default DepartmentForm


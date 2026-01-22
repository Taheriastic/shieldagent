import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import {
  Upload,
  FileText,
  File,
  Trash2,
  AlertCircle,
  CheckCircle,
} from 'lucide-react'
import { Button, Card, CardHeader, CardTitle, CardContent, Badge } from '../components/ui'
import { useDocuments, useUploadDocument, useDeleteDocument } from '../hooks/useDocuments'
import { formatBytes, formatDate } from '../lib/utils'
import { getErrorMessage } from '../lib/axios'

export default function DocumentsPage() {
  const { data, isLoading } = useDocuments()
  const uploadDocument = useUploadDocument()
  const deleteDocument = useDeleteDocument()
  
  const [uploadError, setUploadError] = useState('')
  const [uploadSuccess, setUploadSuccess] = useState('')

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      setUploadError('')
      setUploadSuccess('')

      for (const file of acceptedFiles) {
        try {
          await uploadDocument.mutateAsync(file)
          setUploadSuccess(`${file.name} uploaded successfully`)
        } catch (err) {
          setUploadError(getErrorMessage(err))
        }
      }
    },
    [uploadDocument]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/csv': ['.csv'],
      'application/json': ['.json'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
  })

  const handleDelete = async (documentId: string) => {
    if (confirm('Are you sure you want to delete this document?')) {
      try {
        await deleteDocument.mutateAsync(documentId)
      } catch (err) {
        setUploadError(getErrorMessage(err))
      }
    }
  }

  const getFileIcon = (fileType: string) => {
    switch (fileType) {
      case 'pdf':
        return <FileText className="h-8 w-8 text-red-500" />
      case 'csv':
        return <File className="h-8 w-8 text-green-500" />
      case 'json':
        return <File className="h-8 w-8 text-yellow-500" />
      default:
        return <File className="h-8 w-8 text-gray-500" />
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Documents</h1>
        <p className="text-gray-500 mt-1">
          Upload compliance documents for analysis
        </p>
      </div>

      {/* Alerts */}
      {uploadError && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-700">{uploadError}</p>
        </div>
      )}

      {uploadSuccess && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg flex items-start gap-3">
          <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-green-700">{uploadSuccess}</p>
        </div>
      )}

      {/* Upload Zone */}
      <Card>
        <CardContent className="p-6">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }`}
          >
            <input {...getInputProps()} />
            <Upload
              className={`h-12 w-12 mx-auto mb-4 ${
                isDragActive ? 'text-primary-500' : 'text-gray-400'
              }`}
            />
            {isDragActive ? (
              <p className="text-lg text-primary-600 font-medium">
                Drop files here...
              </p>
            ) : (
              <>
                <p className="text-lg text-gray-700 font-medium">
                  Drop files here or click to upload
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Supports PDF, CSV, and JSON files up to 50MB
                </p>
              </>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Document List */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Uploaded Documents ({data?.total || 0})</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
              <p className="text-gray-500 mt-2">Loading documents...</p>
            </div>
          ) : data?.documents.length === 0 ? (
            <div className="p-8 text-center">
              <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No documents uploaded yet</p>
              <p className="text-sm text-gray-400 mt-1">
                Upload your first document to get started
              </p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {data?.documents.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    {getFileIcon(doc.file_type)}
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {doc.original_filename}
                      </p>
                      <div className="flex items-center gap-3 mt-1">
                        <Badge>{doc.file_type.toUpperCase()}</Badge>
                        <span className="text-xs text-gray-500">
                          {formatBytes(doc.file_size)}
                        </span>
                        <span className="text-xs text-gray-500">
                          {formatDate(doc.uploaded_at)}
                        </span>
                      </div>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(doc.id)}
                    className="text-red-600 hover:text-red-700 hover:bg-red-50"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

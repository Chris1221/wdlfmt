# Generated from WdlV1Parser.g4 by ANTLR 4.12.0
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .WdlV1Parser import WdlV1Parser
else:
    from WdlV1Parser import WdlV1Parser

# This class defines a complete generic visitor for a parse tree produced by WdlV1Parser.


class WdlV1ParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by WdlV1Parser#map_type.
    def visitMap_type(self, ctx: WdlV1Parser.Map_typeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#array_type.
    def visitArray_type(self, ctx: WdlV1Parser.Array_typeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#pair_type.
    def visitPair_type(self, ctx: WdlV1Parser.Pair_typeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#type_base.
    def visitType_base(self, ctx: WdlV1Parser.Type_baseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#wdl_type.
    def visitWdl_type(self, ctx: WdlV1Parser.Wdl_typeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#unbound_decls.
    def visitUnbound_decls(self, ctx: WdlV1Parser.Unbound_declsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#bound_decls.
    def visitBound_decls(self, ctx: WdlV1Parser.Bound_declsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#any_decls.
    def visitAny_decls(self, ctx: WdlV1Parser.Any_declsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#number.
    def visitNumber(self, ctx: WdlV1Parser.NumberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#expression_placeholder_option.
    def visitExpression_placeholder_option(
        self, ctx: WdlV1Parser.Expression_placeholder_optionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#string_part.
    def visitString_part(self, ctx: WdlV1Parser.String_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#string_parts.
    def visitString_parts(self, ctx: WdlV1Parser.String_partsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#string_expr_part.
    def visitString_expr_part(self, ctx: WdlV1Parser.String_expr_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#string_expr_with_string_part.
    def visitString_expr_with_string_part(
        self, ctx: WdlV1Parser.String_expr_with_string_partContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#dquote_string.
    def visitDquote_string(self, ctx: WdlV1Parser.Dquote_stringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#squote_string.
    def visitSquote_string(self, ctx: WdlV1Parser.Squote_stringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#primitive_literal.
    def visitPrimitive_literal(self, ctx: WdlV1Parser.Primitive_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#expr.
    def visitExpr(self, ctx: WdlV1Parser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#infix0.
    def visitInfix0(self, ctx: WdlV1Parser.Infix0Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#infix1.
    def visitInfix1(self, ctx: WdlV1Parser.Infix1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#lor.
    def visitLor(self, ctx: WdlV1Parser.LorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#infix2.
    def visitInfix2(self, ctx: WdlV1Parser.Infix2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#land.
    def visitLand(self, ctx: WdlV1Parser.LandContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#eqeq.
    def visitEqeq(self, ctx: WdlV1Parser.EqeqContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#lt.
    def visitLt(self, ctx: WdlV1Parser.LtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#infix3.
    def visitInfix3(self, ctx: WdlV1Parser.Infix3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#gte.
    def visitGte(self, ctx: WdlV1Parser.GteContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#neq.
    def visitNeq(self, ctx: WdlV1Parser.NeqContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#lte.
    def visitLte(self, ctx: WdlV1Parser.LteContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#gt.
    def visitGt(self, ctx: WdlV1Parser.GtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#add.
    def visitAdd(self, ctx: WdlV1Parser.AddContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#sub.
    def visitSub(self, ctx: WdlV1Parser.SubContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#infix4.
    def visitInfix4(self, ctx: WdlV1Parser.Infix4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#mod.
    def visitMod(self, ctx: WdlV1Parser.ModContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#mul.
    def visitMul(self, ctx: WdlV1Parser.MulContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#divide.
    def visitDivide(self, ctx: WdlV1Parser.DivideContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#infix5.
    def visitInfix5(self, ctx: WdlV1Parser.Infix5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#negate.
    def visitNegate(self, ctx: WdlV1Parser.NegateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#unarysigned.
    def visitUnarysigned(self, ctx: WdlV1Parser.UnarysignedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#infix6.
    def visitInfix6(self, ctx: WdlV1Parser.Infix6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#expr_infix6.
    def visitExpr_infix6(self, ctx: WdlV1Parser.Expr_infix6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#member.
    def visitMember(self, ctx: WdlV1Parser.MemberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#pair_literal.
    def visitPair_literal(self, ctx: WdlV1Parser.Pair_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#primitives.
    def visitPrimitives(self, ctx: WdlV1Parser.PrimitivesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#left_name.
    def visitLeft_name(self, ctx: WdlV1Parser.Left_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#at.
    def visitAt(self, ctx: WdlV1Parser.AtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#apply.
    def visitApply(self, ctx: WdlV1Parser.ApplyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#ifthenelse.
    def visitIfthenelse(self, ctx: WdlV1Parser.IfthenelseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#map_literal.
    def visitMap_literal(self, ctx: WdlV1Parser.Map_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#get_name.
    def visitGet_name(self, ctx: WdlV1Parser.Get_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#object_literal.
    def visitObject_literal(self, ctx: WdlV1Parser.Object_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#array_literal.
    def visitArray_literal(self, ctx: WdlV1Parser.Array_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#expression_group.
    def visitExpression_group(self, ctx: WdlV1Parser.Expression_groupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#version.
    def visitVersion(self, ctx: WdlV1Parser.VersionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#import_alias.
    def visitImport_alias(self, ctx: WdlV1Parser.Import_aliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#import_as.
    def visitImport_as(self, ctx: WdlV1Parser.Import_asContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#import_doc.
    def visitImport_doc(self, ctx: WdlV1Parser.Import_docContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#struct.
    def visitStruct(self, ctx: WdlV1Parser.StructContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_value.
    def visitMeta_value(self, ctx: WdlV1Parser.Meta_valueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_string_part.
    def visitMeta_string_part(self, ctx: WdlV1Parser.Meta_string_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_string_parts.
    def visitMeta_string_parts(self, ctx: WdlV1Parser.Meta_string_partsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_dquote_string.
    def visitMeta_dquote_string(self, ctx: WdlV1Parser.Meta_dquote_stringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_squote_string.
    def visitMeta_squote_string(self, ctx: WdlV1Parser.Meta_squote_stringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_array.
    def visitMeta_array(self, ctx: WdlV1Parser.Meta_arrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_object.
    def visitMeta_object(self, ctx: WdlV1Parser.Meta_objectContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_object_kv.
    def visitMeta_object_kv(self, ctx: WdlV1Parser.Meta_object_kvContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_kv.
    def visitMeta_kv(self, ctx: WdlV1Parser.Meta_kvContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#parameter_meta.
    def visitParameter_meta(self, ctx: WdlV1Parser.Parameter_metaContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta.
    def visitMeta(self, ctx: WdlV1Parser.MetaContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_runtime_kv.
    def visitTask_runtime_kv(self, ctx: WdlV1Parser.Task_runtime_kvContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_runtime.
    def visitTask_runtime(self, ctx: WdlV1Parser.Task_runtimeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_input.
    def visitTask_input(self, ctx: WdlV1Parser.Task_inputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_output.
    def visitTask_output(self, ctx: WdlV1Parser.Task_outputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_command_string_parts.
    def visitTask_command_string_parts(
        self, ctx: WdlV1Parser.Task_command_string_partsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_command_expr_part.
    def visitTask_command_expr_part(
        self, ctx: WdlV1Parser.Task_command_expr_partContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_command_expr_with_string.
    def visitTask_command_expr_with_string(
        self, ctx: WdlV1Parser.Task_command_expr_with_stringContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_command.
    def visitTask_command(self, ctx: WdlV1Parser.Task_commandContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task_element.
    def visitTask_element(self, ctx: WdlV1Parser.Task_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#task.
    def visitTask(self, ctx: WdlV1Parser.TaskContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#inner_workflow_element.
    def visitInner_workflow_element(
        self, ctx: WdlV1Parser.Inner_workflow_elementContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#call_alias.
    def visitCall_alias(self, ctx: WdlV1Parser.Call_aliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#call_input.
    def visitCall_input(self, ctx: WdlV1Parser.Call_inputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#call_inputs.
    def visitCall_inputs(self, ctx: WdlV1Parser.Call_inputsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#call_body.
    def visitCall_body(self, ctx: WdlV1Parser.Call_bodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#call_name.
    def visitCall_name(self, ctx: WdlV1Parser.Call_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#call.
    def visitCall(self, ctx: WdlV1Parser.CallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#scatter.
    def visitScatter(self, ctx: WdlV1Parser.ScatterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#conditional.
    def visitConditional(self, ctx: WdlV1Parser.ConditionalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#workflow_input.
    def visitWorkflow_input(self, ctx: WdlV1Parser.Workflow_inputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#workflow_output.
    def visitWorkflow_output(self, ctx: WdlV1Parser.Workflow_outputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#input.
    def visitInput(self, ctx: WdlV1Parser.InputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#output.
    def visitOutput(self, ctx: WdlV1Parser.OutputContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#inner_element.
    def visitInner_element(self, ctx: WdlV1Parser.Inner_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#parameter_meta_element.
    def visitParameter_meta_element(
        self, ctx: WdlV1Parser.Parameter_meta_elementContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#meta_element.
    def visitMeta_element(self, ctx: WdlV1Parser.Meta_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#workflow.
    def visitWorkflow(self, ctx: WdlV1Parser.WorkflowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#document_element.
    def visitDocument_element(self, ctx: WdlV1Parser.Document_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#document.
    def visitDocument(self, ctx: WdlV1Parser.DocumentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#type_document.
    def visitType_document(self, ctx: WdlV1Parser.Type_documentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by WdlV1Parser#expr_document.
    def visitExpr_document(self, ctx: WdlV1Parser.Expr_documentContext):
        return self.visitChildren(ctx)


del WdlV1Parser
